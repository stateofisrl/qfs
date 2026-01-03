# Generated manually for withdrawal fee in referrals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0003_welcome_bonus'),
    ]

    operations = [
        migrations.AddField(
            model_name='referralsettings',
            name='withdrawal_fee_percentage',
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                help_text='Withdrawal fee percentage for users who received welcome bonus (0 = no fee)',
                max_digits=5,
            ),
        ),
    ]
