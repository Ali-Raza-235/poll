from django.urls import path
from .views import PollCreateAPIView

urlpatterns = [
    path('polls/', PollCreateAPIView.as_view(), name='poll-create'),
]
