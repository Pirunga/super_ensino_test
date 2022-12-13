from django.core.management.base import BaseCommand
from os import getenv
from questions.models import User

class Command(BaseCommand):
    """
    Create superuser.
    """
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = getenv('DJANGO_SUPERUSER_USERNAME')
            email = getenv('DJANGO_SUPERUSER_EMAIL')
            password = getenv('DJANGO_SUPERUSER_PASSWORD')
            print('Creating account for %s (%s)' % (username, email))

            admin = User.objects.create_superuser(
                email=email,
                username=username,
                password=password
            )
            admin.is_active = True
            admin.is_admin = True
            admin.save()
