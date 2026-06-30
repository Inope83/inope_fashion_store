from django.core.management.base import BaseCommand
from apps.users.models import Kliente, Admin


class Command(BaseCommand):
    help = 'Kria administrador foun'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email administrador')
        parser.add_argument('password', type=str, help='Liafuan-pase')
        parser.add_argument('--naran', type=str, default='Admin', help='Naran administrador')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        naran = options['naran']

        if Kliente.objects.filter(email=email).exists():
            self.stderr.write(self.style.ERROR(f'Kliente ho email "{email}" iha tiha ona'))
            return

        kliente = Kliente(naran=naran, email=email, password=password, is_staff=True)
        kliente.save()

        Admin.objects.get_or_create(username=email, defaults={'password': password})

        self.stdout.write(self.style.SUCCESS(f'Administrador "{naran}" ({email}) kria ho suksesu!'))
