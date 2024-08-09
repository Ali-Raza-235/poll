from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from .models import Poll
from .serializers import PollSerializer, PollUpdateSerializer

# Create your views here.

class PollView(ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get(self, request, *args, **kwargs):
        return render(request, 'create_poll.html')

class DeletePollView(DestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    lookup_field = 'id'

class UpdatePollView(UpdateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollUpdateSerializer
    lookup_field = 'id'
