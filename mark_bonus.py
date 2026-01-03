import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
import django
django.setup()
from apps.users.models import CustomUser

u = CustomUser.objects.get(email='noobodii6@gmail.com')
u.received_welcome_bonus = True
u.save(update_fields=['received_welcome_bonus'])
print('Marked noobodii6@gmail.com as received_welcome_bonus=True')
