from django.urls import path
from .views import CreatePollView, DeletePollView, UpdatePollView, ListUserPollsView, RegisterView, LogoutView, LoginView

urlpatterns = [
    path('create-poll/', CreatePollView.as_view(), name='create_poll'),
    path('user-polls', ListUserPollsView.as_view(), name='user_polls'),
    path('update-poll/<int:id>/', UpdatePollView.as_view(), name='poll_update'),
    path('delete-poll/<int:id>/', DeletePollView.as_view(), name='poll_delete'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
