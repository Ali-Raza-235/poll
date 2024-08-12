from django.shortcuts import render, redirect
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from .models import Poll, User, Question
from .serializers import PollSerializer, PollUpdateSerializer
from django.contrib import messages

# Create your views here.

class PollView(ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get(self, request):
        return render(request, 'create_poll.html')
    
    def post(self, request):
        if request.method == "POST":
            creator_email = request.POST.get('creator')
            poll_title = request.POST.get('poll')
            questions_data = request.POST.getlist('questions')

            try:
                creator = User.objects.get(email=creator_email)
            except User.DoesNotExist:
                creator = User.objects.create(email=creator_email)

            poll = Poll.objects.create(title=poll_title, creater=creator)

            question_index = 1
            while f'questions[{question_index}][question]' in request.POST:
                question_text = request.POST.get(f'questions[{question_index}][question]')
                option1 = request.POST.get(f'questions[{question_index}][option1]')
                option2 = request.POST.get(f'questions[{question_index}][option2]')
                option3 = request.POST.get(f'questions[{question_index}][option3]')

                options = [option1, option2, option3]

                if question_text:
                    question = Question.objects.create(title=question_text, choices=','.join(options))
                    poll.questions.add(question)

                question_index += 1

            poll.save()

            messages.success(request, 'Poll has been Created Sucessfully!')

            return redirect('/')

        return render(request, 'create_poll.html')


class DeletePollView(DestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    lookup_field = 'id'

class UpdatePollView(UpdateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollUpdateSerializer
    lookup_field = 'id'
