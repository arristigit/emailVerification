from django.contrib.messages.api import error
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login', login_attempt, name='login_attempt'),
    path('register', register_attempt, name='register_attempt'),
    path('token', token, name='token'),
    path('success', success, name='success'),
    path('verify/<auth_token>', verify, name='verify'),
    path('error', error_page, name='error'),
    path('logout', logout_attempt, name='logout_attempt'),
    path('forgotpass', forgotpass, name='forgotpass'),
]