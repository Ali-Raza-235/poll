from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from .models import Poll, User, Question, PollAnswer, PollResponse
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

def list_polls(request):
    polls = Poll.objects.all()
    return render(request, 'list_polls.html', {'polls': polls})

def poll_detail(request, id):
    poll = get_object_or_404(Poll, id=id)
    questions = poll.questions.all()

    question_data = []

    for question in questions:
        choices = question.choices.split(',')
        question_data.append({
            "id": question.id,
            'title': question.title,
            'choices': choices,
        })

    if request.method == "POST":
        user_email = request.POST.get('user_email')

        poll_response, created = PollResponse.objects.get_or_create(
            poll=poll,
            user_email=user_email,
        )

        for question in questions:
            answer = request.POST.get(f'question_{question.id}')
            if answer:
                PollAnswer.objects.update_or_create(
                    response=poll_response,
                    question=question,
                    defaults={'answer': answer}
                )

        messages.success(request, 'Your responses have been submitted successfully!')
        return redirect('/')

    context = {'poll': poll, 'questions': question_data}

    return render(request, 'poll_detail.html', context=context)

def poll_responses(request, id):
    poll = get_object_or_404(Poll, id=id)
    responses = PollResponse.objects.filter(poll=poll)

    context = {
        "poll": poll,
        "responses": responses,
    }

    return render(request, 'response_list.html', context=context)