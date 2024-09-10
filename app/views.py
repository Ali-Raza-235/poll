from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics, status
from .models import Poll, User, Question, PollAnswer, PollResponse
from .serializers import PollSerializer, PollUpdateSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token

# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PollPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 100

class PollView(generics.ListCreateAPIView):
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

class DeletePollView(APIView):
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
                return Response({"message": "Poll deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            except Poll.DoesNotExist:
                return Response({"message": "Poll not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Please provide a poll ID to delete."}, status=status.HTTP_400_BAD_REQUEST)



class UpdatePollView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_polls = Poll.objects.filter(creater=request.user)
        if not user_polls.exists():
            return Response({"message": "You don't have any polls to update."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PollSerializer(user_polls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        poll_id = kwargs.get('id', None)
        if poll_id:
            try:
                poll = Poll.objects.get(id=poll_id)
                if poll.creater != request.user:
                    raise PermissionDenied("You do not have permission to update this poll.")
                
                serializer = PollUpdateSerializer(poll, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Poll.DoesNotExist:
                return Response({"message": "Poll not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Please provide a poll ID to update."}, status=status.HTTP_400_BAD_REQUEST)


class ListUserPollsView(generics.ListAPIView):
    serializer_class = PollSerializer
    pagination_class = PollPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Poll.objects.filter(creater=self.request.user)

class ListPollsView(generics.ListAPIView):
    pagination_class = PollPagination
    serializer_class = PollSerializer

    def get(self, request):
        polls = Poll.objects.all().order_by('-is_open')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(polls, request)
        serializer = self.serializer_class(page, many=True)
        
        context = {
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