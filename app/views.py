from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Poll
from .serializers import PollSerializer

# Create your views here.

class PollView(ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class DetialPollView(RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    http_method_names = ['put', 'delete']
    lookup_field = 'id'
