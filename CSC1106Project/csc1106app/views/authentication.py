import base64

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from ..forms import ChangePasswordForm, CustomAuthenticationForm
from ..models import Employee
from ..models import UserSession
from django.contrib.sessions.models import Session



# Home View
def index(request):
    return render(request, 'index.html')

@login_required
def settings(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully")
            return redirect('home')
        else:
            message = "";
            for field, errors in form.errors.items():
                for error in errors:
                    message += f"{error}\n"

            messages.error(request, message, extra_tags='danger')
    else:
        form = ChangePasswordForm(request.user)


    return render(request, 'settings.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user and user.is_locked:
                messages.error(request, "Your account has been locked. Please contact HR to unlock your account.")

            elif user is not None and user.is_active:
                employee = Employee.objects.get(user=user)
                login(request, user)
                
                if not employee.onboarded:
                    return redirect('onboard')

                return redirect('home')  # Redirect to a home page or another page after login

        else:
            # Handle invalid login attempt
            error_message = "Invalid username or password."
            messages.error(request, error_message)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def onboard(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        image_data = request.POST.get('image-data')
        if image_data and form.is_valid():
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            user_identifier = request.user.email

            # This is the image data to post into
            data = ContentFile(base64.b64decode(imgstr), name=f'{user_identifier}_checkin.{ext}')

            try:
                employee = Employee.objects.get(user=request.user)
                employee.image = data
                employee.onboarded = True
                user = form.save()
                update_session_auth_hash(request, user)
                employee.save()
                messages.success(request, 'Successfully onboarded. Welcome to the company.')
                return redirect('home')
            except Employee.DoesNotExist:
                messages.error('Employee not found')

    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'onboard.html', {'form': form})

def logout_user(request):
    usersession = UserSession.objects.get(session_id=request.session.session_key)

    if usersession:
        usersession.delete()

    logout(request)
    return redirect('login')

