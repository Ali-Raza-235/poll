from django.urls import path
from .views import PollView, DeletePollView, UpdatePollView

urlpatterns = [
    path('polls/', PollView.as_view(), name='create-list-poll'),
    path('polls/<int:id>/', UpdatePollView.as_view(), name='update-poll'),
    path('polls/<int:id>/delete/', DeletePollView.as_view(), name='delete-poll'),
]
