from django.urls import path

from .views import RegisterUserView, UsersListCreateView

urlpatterns = [
    path('', UsersListCreateView.as_view(), name='users_list'),
    path('/me', RegisterUserView.as_view(), name='user_register'),
]