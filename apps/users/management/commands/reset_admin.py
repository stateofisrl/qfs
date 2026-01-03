from django.core.management.base import BaseCommand
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = 'Reset admin password'

    def handle(self, *args, **options):
        try:
            # Get or create admin user
            user, created = CustomUser.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'stateofisrl@gmail.com',
                    'is_staff': True,
                    'is_superuser': True,
                    'is_active': True,
                }
            )
            
            # Set password
            user.set_password('adaadmin5199')
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            
            action = 'Created' if created else 'Updated'
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ {action} admin user successfully!\n'
                    f'Username: {user.username}\n'
                    f'Email: {user.email}\n'
                    f'Password: adaadmin5199\n'
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
