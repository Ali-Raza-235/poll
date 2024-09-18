from django.urls import path
from app import views

urlpatterns = [
    path('polls/', views.PollView.as_view(), name='create-list-poll'),
    path('polls/<int:id>/', views.UpdatePollView.as_view(), name='update-poll'),
    path('polls/<int:id>/delete/', views.DeletePollView.as_view(), name='delete-poll'),
    path('open-polls/', views.get_open_polls_raw, name='open_polls'),
    path('closed-polls/', views.get_closed_polls_cursor, name='closed_polls'),
    path('polls/<int:poll_id>/detail/', views.get_poll_with_user_detail, name='poll_detail'),
    path('polls/stats/', views.get_poll_stats, name='poll_stats'),
]
