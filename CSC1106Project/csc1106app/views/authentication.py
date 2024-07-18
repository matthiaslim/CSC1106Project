import base64

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from ..forms import ChangePasswordForm, CustomAuthenticationForm
from ..models import Employee


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
            return redirect('home')
    else:
        form = ChangePasswordForm(request.user)


    return render(request, 'settings.html', {'form': form})


# Login View
def login_user(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_active:
                employee = Employee.objects.get(user=user)
                login(request, user)
                if not employee.onboarded:
                    return redirect('onboard')

                return redirect('home')  # Redirect to a home page or another page after login
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

# def register_user(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')  # Redirect to a home page or another page after signup
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'signup.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

