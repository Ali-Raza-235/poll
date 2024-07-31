from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Poll
from .serializers import PollSerializer

# Create your views here.
class PollAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 200, 'payload': serializer.data, 'message': "Your Data has been Saved Successfully"})
        return Response({'status': 403, 'errors': serializer.errors, 'message': "Something Went Wrong"})

    
    def get(self, request, *args, **kwargs):
        poll_obj = Poll.objects.all()
        serializer = PollSerializer(poll_obj, many=True)

        return Response({'status': 200, 'payload': serializer.data})
    
    
    def put(self, request, *args, **kwargs):
        try:
            poll_obj = Poll.objects.get(id=request.data['id'])
            serializer = PollSerializer(poll_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 200, 'payload': serializer.data, 'message': 'Your data has been updated successfully.'})
            
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})
        except:
            return Response({'status': 403, 'message': 'Invalid ID'})
        
    def patch(self, request, *args, **kwargs):
        try:
            poll_obj = Poll.objects.get(id=request.data['id'])
            serializer = PollSerializer(poll_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 200, 'payload': serializer.data, 'message': 'Your data has been updated successfully.'})
            
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})
        except:
            return Response({'status': 403, 'message': 'Invalid ID'})
        
    def delete(self, request, *args, **kwargs):
        try:
            poll_obj = Poll.objects.get(id=request.data['id'])
            poll_obj.delete()
            return Response({'status':200, 'message': 'Record has been Deleted Successfully!'})
        except:
            return Response({'status': 403, 'message': 'Invalid ID'})
