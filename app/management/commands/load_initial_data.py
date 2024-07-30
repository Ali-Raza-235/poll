from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import User, Poll, Question


class Command(BaseCommand):
    help = 'Load initial data into the database'

    @transaction.atomic
    def handle(self, *args, **options):
        # Check if user exists, create if it does not
        user, created = User.objects.get_or_create(
            email='testuser@example.com',
            defaults={
                'username': 'testuser',  # Make sure this is unique
                'first_name': 'name1',
                'last_name': 'name2',
                'password': 'password123'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Initial user data loaded successfully.'))
        else:
            self.stdout.write(self.style.WARNING('User already exists.'))

        # Create questions
        question1 = Question.objects.create(
            title='What is your favorite color?',
            choices='Red,Blue,Green,Yellow'
        )
        question2 = Question.objects.create(
            title='What is your favorite animal?',
            choices='Cat,Dog,Elephant,Lion'
        )

        # Create a poll
        poll = Poll.objects.create(
            title='General Knowledge Poll',
            creater=user,
            is_open=True
        )
        poll.questions.set([question1, question2])
        poll.save()

        self.stdout.write(self.style.SUCCESS('Initial poll data loaded successfully.'))
