# Generated manually for withdrawal fee field
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('withdrawals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawal',
            name='withdrawal_fee',
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                help_text='Fee charged for withdrawal (only for welcome bonus recipients)',
                max_digits=15,
            ),
        ),
    ]
