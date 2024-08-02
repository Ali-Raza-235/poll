from django.urls import path
from .views import PollView, DetialPollView

urlpatterns = [
    path('polls/', PollView.as_view(), name='creat-list-poll'),
    path('polls/<int:id>/', DetialPollView.as_view(), name='update-delete-poll'),
    # path('polls/<int:id>/', PollAPIView.as_view(), name='poll-detail'),
]
