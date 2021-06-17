from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from .models import Profile
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required(login_url="/")
def home(request):
    return render(request, 'accounts/home.html')

def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(username, email, password)

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is taken')
                return redirect('/register')
            
            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is taken')
                return redirect('/register')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj, auth_token= auth_token)
            profile_obj.save()

            send_mail_after_registeration(email, auth_token, username)

            return redirect('/token')
        
        except Exception as e:
            print(e)

    return render(request, 'accounts/register.html')

def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/login')

        profile_obj = Profile.objects.filter(user=user_obj).first()
        
        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified. Please check your mail.')
            return redirect('/login')
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/login')

        login(request, user)
        return redirect('/success')


    return render(request, 'accounts/login.html')

def token(request):
    return render(request, 'accounts/token.html')

def success(request):
    return render(request, 'accounts/success.html')

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/login')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified succefully.')
            return redirect('/login')
        else:
            messages.success(request, 'Your account verificaton unsuccefully. Try again!')
            return redirect('/error')
    except Exception as e:
        print(e)

def forgotpass(request):
    return render(request, 'accounts/forgotpass.html')

def error_page(request):
    return render(request, 'accounts/error.html')

def logout_attempt(request):
    logout(request)
    messages.success(request, 'You are successfully logout.')
    return render(request, 'accounts/logout.html')

def send_mail_after_registeration(email, token, username):
    subject = 'Your accounts need to be verified'
    message = f'Dear {username}, Click on the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)