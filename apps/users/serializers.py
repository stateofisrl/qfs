"""
User serializers.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from decimal import Decimal

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )
    referral_code = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        help_text="Referral code of the user who referred you"
    )
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name', 'referral_code']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate_referral_code(self, value):
        """Validate referral code exists if provided."""
        if value:
            if not User.objects.filter(referral_code=value).exists():
                raise serializers.ValidationError('Invalid referral code.')
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs
    
    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        bonus_info = None

        # Create referral relationship and apply welcome bonus if configured
        if referral_code:
            from apps.referrals.models import Referral, ReferralSettings, CommissionTransaction
            try:
                referrer = User.objects.get(referral_code=referral_code)
                Referral.objects.create(referrer=referrer, referred=user)

                settings = ReferralSettings.objects.first()
                if (
                    settings
                    and settings.is_active
                    and settings.welcome_bonus_enabled
                    and settings.welcome_bonus_amount > 0
                ):
                    bonus_amount = settings.welcome_bonus_amount
                    user.balance = Decimal(user.balance or 0) + Decimal(bonus_amount)
                    user.total_earnings = Decimal(user.total_earnings or 0) + Decimal(bonus_amount)
                    user.save(update_fields=['balance', 'total_earnings'])

                    CommissionTransaction.objects.create(
                        commission=None,
                        user=user,
                        amount=bonus_amount,
                        transaction_type='welcome_bonus'
                    )

                    # Mark user as received bonus
                    user.received_welcome_bonus = True
                    user.save(update_fields=['received_welcome_bonus'])

                    bonus_info = {
                        'amount': str(bonus_amount),
                        'message': settings.welcome_bonus_message,
                    }

            except User.DoesNotExist:
                pass  # Already validated, so this shouldn't happen

        if bonus_info:
            # Expose bonus info back to the view for response payloads
            self.context['welcome_bonus_info'] = bonus_info
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    total_referrals = serializers.SerializerMethodField()
    total_referral_earnings = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'balance', 'total_invested', 'total_earnings', 'is_verified',
            'phone_number', 'country', 'profile_image', 'referral_code',
            'total_referrals', 'total_referral_earnings', 'created_at'
        ]
        read_only_fields = [
            'id', 'balance', 'total_invested', 'total_earnings',
            'is_verified', 'referral_code', 'created_at'
        ]
    
    def get_total_referrals(self, obj):
        """Get count of users referred by this user."""
        return obj.referrals_made.count()
    
    def get_total_referral_earnings(self, obj):
        """Get total earnings from referrals."""
        from apps.referrals.models import ReferralCommission
        total = sum(
            c.amount for c in ReferralCommission.objects.filter(
                referral__referrer=obj,
                status='paid'
            )
        )
        return float(total)


class UserUpdateSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 
            'country', 'profile_image'
        ]


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
