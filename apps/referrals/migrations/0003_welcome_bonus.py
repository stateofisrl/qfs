# Generated manually for welcome bonus support
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('referrals', '0002_commissiontransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='referralsettings',
            name='welcome_bonus_amount',
            field=models.DecimalField(
                decimal_places=2,
                default=0.00,
                help_text="Bonus amount credited to referred user's balance upon signup",
                max_digits=15,
            ),
        ),
        migrations.AddField(
            model_name='referralsettings',
            name='welcome_bonus_enabled',
            field=models.BooleanField(
                default=False,
                help_text='Give a signup bonus to users who register with a referral code',
            ),
        ),
        migrations.AddField(
            model_name='referralsettings',
            name='welcome_bonus_message',
            field=models.CharField(
                default='Welcome bonus credited for joining via referral',
                help_text='Notification text shown to the new user when bonus is applied',
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name='commissiontransaction',
            name='commission',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='transactions',
                to='referrals.referralcommission',
            ),
        ),
        migrations.AlterField(
            model_name='commissiontransaction',
            name='transaction_type',
            field=models.CharField(
                choices=[
                    ('commission_earned', 'Commission Earned'),
                    ('commission_paid', 'Commission Paid'),
                    ('commission_cancelled', 'Commission Cancelled'),
                    ('welcome_bonus', 'Welcome Bonus'),
                ],
                default='commission_earned',
                max_length=20,
            ),
        ),
    ]
