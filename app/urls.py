from django.urls import path
from .views import PollView, DeletePollView, UpdatePollView, ListUserPollsView, RegisterView

urlpatterns = [
    path('polls/', PollView.as_view(), name='poll_list_create'),
    path('polls/my/', ListUserPollsView.as_view(), name='user_polls'),
    path('polls/update/<int:id>/', UpdatePollView.as_view(), name='poll_update'),
    path('polls/delete/<int:id>/', DeletePollView.as_view(), name='poll_delete'),
    path('register/', RegisterView.as_view(), name='register'),
]
