from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics, status
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib import messages, auth
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
from .models import Poll, User, Question, PollAnswer, PollResponse
from .serializers import PollSerializer, RegisterSerializer, LoginSerializer
from django.db import transaction

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return redirect('/')
        return render(request, 'register.html', {'errors': serializer.errors})

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def get(self, request, format=None):
        return render(request, 'login.html')

    def post(self, request, format=None):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            response = redirect('/')  # Adjust this to your desired redirect URL
            response.set_cookie(key='auth_token', value=token.key)
            return response
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

class LogoutView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        auth.logout(request)
        return redirect('login')

class PollPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 100

class CreatePollView(LoginRequiredMixin, generics.CreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'create_poll.html')
    
    def post(self, request):
        if request.user.is_authenticated:
            creator_email = request.user.email
        else:
            creator_email = request.POST.get('creator')
        poll_title = request.POST.get('poll')
        questions_data = request.POST.getlist('questions')

        creator, created = User.objects.get_or_create(email=creator_email)

        poll = Poll.objects.create(title=poll_title, creater=creator)

        question_index = 1
        while f'questions[{question_index}][question]' in request.POST:
            question_text = request.POST.get(f'questions[{question_index}][question]')
            options = [request.POST.get(f'questions[{question_index}][option{i+1}]') for i in range(3)]

            if question_text:
                question = Question.objects.create(title=question_text, choices=','.join(filter(None, options)))
                poll.questions.add(question)

            question_index += 1

        poll.save()

        messages.success(request, 'Poll has been Created Successfully!')
        return redirect('/')

class DeletePollView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_polls = Poll.objects.filter(creater=request.user)
        if not user_polls.exists():
            return Response({"message": "You don't have any polls to delete."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PollSerializer(user_polls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        poll_id = kwargs.get('id', None)
        if poll_id:
            try:
                poll = Poll.objects.get(id=poll_id)
                if poll.creater != request.user:
                    raise PermissionDenied("You do not have permission to delete this poll.")
                poll.delete()
                messages.success(request, 'Poll deleted successfully.')
                return redirect('user_polls')
            except Poll.DoesNotExist:
                return Response({"message": "Poll not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Please provide a poll ID to delete."}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class UpdatePollView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        poll_id = kwargs.get('id', None)
        if poll_id:
            try:
                poll = Poll.objects.get(id=poll_id, creater=request.user)
                questions = poll.questions.all()

                question_data = [{'id': q.id, 'title': q.title, 'choices': q.choices.split(',')} for q in questions]

                context = {
                    'poll': poll,
                    'questions': question_data,
                }
                return render(request, 'update_poll.html', context)
            except Poll.DoesNotExist:
                return Response({"message": "Poll not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Please provide a poll ID to update."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        poll_id = kwargs.get('id', None)
        if poll_id:
            try:
                poll = Poll.objects.get(id=poll_id, creater=request.user)

                # Update the poll title
                poll.title = request.POST.get('poll', poll.title)

                # Delete old questions
                poll.questions.all().delete()

                question_index = 1
                while f'questions[{question_index}][question]' in request.POST:
                    question_text = request.POST.get(f'questions[{question_index}][question]')
                    options = [request.POST.get(f'questions[{question_index}][option{i+1}]') for i in range(3)]

                    # Ensure question text is not empty
                    if question_text:
                        # Create the question with title and choices
                        question = Question.objects.create(title=question_text.strip(), choices=','.join(filter(None, options)))
                        poll.questions.add(question)

                    question_index += 1

                poll.save()

                messages.success(request, 'Poll has been updated successfully!')
                return redirect('user_polls')
            except Poll.DoesNotExist:
                return Response({"message": "Poll not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Please provide a poll ID to update."}, status=status.HTTP_400_BAD_REQUEST)


class ListUserPollsView(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = PollSerializer
    pagination_class = PollPagination
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        polls = Poll.objects.filter(creater=request.user)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(polls, request)
        serializer = self.serializer_class(page, many=True)
        
        context = {
            'page_obj': paginator.get_paginated_response(serializer.data).data,
            'paginator': paginator,
        }
        return render(request, 'user_polls.html', context)

class TogglePollStatusView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        poll = get_object_or_404(Poll, id=id, creater=request.user)
        poll.is_open = not poll.is_open  # Toggle the is_open field
        poll.save()
        messages.success(request, 'Poll status updated successfully!')
        return redirect('user_polls')

class ListPollsView(generics.ListAPIView):
    pagination_class = PollPagination
    serializer_class = PollSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        polls = Poll.objects.filter(is_open=True).order_by('-id')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(polls, request)
        serializer = self.serializer_class(page, many=True)
        
        context = {
            'page_obj': paginator.get_paginated_response(serializer.data).data,
            'paginator': paginator,
        }
        return render(request, 'list_polls.html', context)

@login_required
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

        poll_response, created = PollResponse.objects.get_or_create(
            poll=poll,
            user_email=request.user.email,
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