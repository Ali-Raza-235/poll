from django.urls import path
from .views import PollAPIView

urlpatterns = [
    path('polls/', PollAPIView.as_view(), name='poll-create'),
    path('polls/<int:id>/', PollAPIView.as_view(), name='poll-detail'),
]
