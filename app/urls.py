from django.urls import path
from .views import CreatePollView, DeletePollView, UpdatePollView, ListUserPollsView, TogglePollStatusView, RegisterView, LogoutView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/polls', ListUserPollsView.as_view(), name='user_polls'),
    path('create/poll/', CreatePollView.as_view(), name='create_poll'),
    path('update/poll/<int:id>/', UpdatePollView.as_view(), name='poll_update'),
    path('delete/poll/<int:id>/', DeletePollView.as_view(), name='poll_delete'),
    path('polls/toggle/<int:id>/', TogglePollStatusView.as_view(), name='poll_toggle'),
]
