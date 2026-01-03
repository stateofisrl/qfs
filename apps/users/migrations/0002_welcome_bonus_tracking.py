# Generated manually for welcome bonus tracking support
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='received_welcome_bonus',
            field=models.BooleanField(
                default=False,
                help_text='User received welcome bonus from referral signup',
            ),
        ),
    ]
