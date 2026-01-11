from django.core.management import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = CustomUser.objects.create(phone_number="89871371048")
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.set_password("1990")
        user.save()
