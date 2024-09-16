from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from .models import Poll, User, Question, PollAnswer, PollResponse
from .serializers import PollSerializer, PollUpdateSerializer
from rest_framework.pagination import PageNumberPagination
from django.contrib import messages
from django.db import connection

# Create your views here.

class PollPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 100

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

class ListPollsView(ListAPIView):
    pagination_class = PollPagination
    serializer_class = PollSerializer

    def get(self, request):
        polls = Poll.objects.all().order_by('-is_open')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(polls, request)
        serializer = self.serializer_class(page, many=True)

        poll_data = [{'id': poll.id, 'title': poll.title, 'creater_id': poll.creater.id, 'is_open': poll.is_open} for poll in page]
        
        context = {
            'polls': poll_data,
            'page_obj': paginator.get_paginated_response(serializer.data).data,
            'paginator': paginator,
        }
        return render(request, 'list_polls.html', context)

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


# Using raw() method to fetch open polls
def get_open_polls_raw(request):
    open_polls = Poll.objects.raw('SELECT * FROM app_poll WHERE is_open == %s', [True])

    # Prepare poll data similar to queryset
    poll_data = [{'id': poll.id, 'title': poll.title, 'creater_id': poll.creater.id, 'is_open': poll.is_open} for poll in open_polls]
    
    # Standard context format
    context = {'polls': poll_data}

    return render(request, 'list_polls.html', context)

# Using connection.cursor() to fetch closed polls
def get_closed_polls_cursor(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM app_poll WHERE is_open = %s", [False])
        closed_polls = cursor.fetchall()

    # Structure the data like queryset
    poll_data = [{'id': row[0], 'title': row[1], 'creater_id': row[2], 'is_open': row[3]} for row in closed_polls]
    
    # Standard context format
    context = {'polls': poll_data}

    return render(request, 'list_polls.html', context)