from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Poll
from .serializers import PollSerializer

# Create your views here.
class PollCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 200, 'payload': serializer.data, 'message': "Your Data has been Saved Successfully"})
        return Response({'status': 403, 'errors': serializer.errors, 'message': "Something Went Wrong"})


