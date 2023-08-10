from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, UserUpdateView, generate_new_password, RegisterView, \
    verification_new_user, send_new_verification_code

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('profile/verification/<int:pk>', verification_new_user, name='verification_new_user'),
    path('profile/send_verification/<int:pk>', send_new_verification_code, name='send_verification'),

]