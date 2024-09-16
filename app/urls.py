from django.urls import path
from .views import PollView, DeletePollView, UpdatePollView, get_closed_polls_cursor, get_open_polls_raw

urlpatterns = [
    path('polls/', PollView.as_view(), name='create-list-poll'),
    path('polls/<int:id>/', UpdatePollView.as_view(), name='update-poll'),
    path('polls/<int:id>/delete/', DeletePollView.as_view(), name='delete-poll'),
    path('open-polls/', get_open_polls_raw, name='open_polls'),
    path('closed-polls/', get_closed_polls_cursor, name='closed_polls'),
]
