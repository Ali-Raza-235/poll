from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import User, Poll, Question

class Command(BaseCommand):
    help = 'Load initial data into the database'

    @transaction.atomic
    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email='testuser@example.com',
            defaults={
                'username': 'testuser',
                'first_name': 'name1',
                'last_name': 'name2',
                'password': 'password123'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Initial user data loaded successfully.'))
        else:
            self.stdout.write(self.style.WARNING('User already exists.'))

        questions = [
            Question(title='What is your favorite color?', choices='Red,Blue,Green,Yellow'),
            Question(title='What is your favorite animal?', choices='Cat,Dog,Elephant,Lion'),
        ]
        
        Question.objects.bulk_create(questions)

        question1 = Question.objects.get(title='What is your favorite color?')
        question2 = Question.objects.get(title='What is your favorite animal?')

        poll = Poll.objects.create(
            title='General Knowledge Poll',
            creater=user,
            is_open=True
        )
        poll.questions.set([question1, question2])
        poll.save()

        self.stdout.write(self.style.SUCCESS('Initial poll data loaded successfully.'))
