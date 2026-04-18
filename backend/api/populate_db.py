from django.core.management.base import BaseCommand
from django.utils import loren_ipsum
from django.contrib.auth.models import User
from .models import Team, Project, Task, Milestone, Note


class Command(BaseCommand):
    help = 'Populates data in database.'

    def handle(self, *args, **kwargs):
        # get or create superuser
        user = User.objects.filter(username='admin').first()

        if not user:
            user = User.objects.create_superuser(
                username='admin', 
                email='admin@email.com',
                password='adminpassword'
            )

        users = [
            User(name='Alice', email='alice@email.com', password='e5&L@IA31'),
            User(name='Mickey', email='mickey@email.com', password='K35@m09sI1'),
            User(name='Minnie', email='minnie@email.com', password='b$l#pW98Af'),
            User(name='Donald', email='donald@email.com', password='h&we$09vS3'),
            User(name='Daisy', email='daisy@email.com', password='4sa@lsM52G')
        ]

        User.objects.bulk_create(users)