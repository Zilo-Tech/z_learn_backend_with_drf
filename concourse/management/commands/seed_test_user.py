from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from concourse.models import Concourse, ConcourseRegistration

class Command(BaseCommand):
    help = 'Create a test user enrolled in all concours.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'testuser'
        email = 'testuser@example.com'
        password = 'testpassword123'
        phone_number = '600000000'

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_active': True,
            }
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))

        concours = Concourse.objects.all()
        for c in concours:
            reg, reg_created = ConcourseRegistration.objects.get_or_create(
                user=user,
                concourse=c,
                defaults={
                    'payment_status': True,
                    'payment_service': 'MTN',
                    'phoneNumber': phone_number,
                }
            )
            if reg_created:
                self.stdout.write(self.style.SUCCESS(f'Enrolled in {c.concourseName}'))
            else:
                self.stdout.write(self.style.WARNING(f'Already enrolled in {c.concourseName}'))

        self.stdout.write(self.style.SUCCESS('Test user setup complete.'))
        self.stdout.write(self.style.SUCCESS(f'Username: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
