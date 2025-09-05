from django.urls import path

from .views import RegisterUserView, UsersListCreateView, UsersRetrieveUpdateDestroyView

urlpatterns = [
    path('', UsersListCreateView.as_view(), name='users_list'),
    path('/me', RegisterUserView.as_view(), name='user_register'),

    path('/info', UsersRetrieveUpdateDestroyView.as_view(), name='user_info'),
]