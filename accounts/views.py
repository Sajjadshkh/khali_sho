from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .forms import RegisterForm, LoginForm
from django.http import JsonResponse

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # 🔐 پاک کردن تایید OTP بعد از استفاده
            request.session.pop('otp_verified', None)
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:home')
        else:
            return render(request, 'accounts/login.html', {'error': True})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('home:home')


def ajax_login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/'})
        else:
            return JsonResponse({'success': False, 'error': 'نام کاربری یا رمز اشتباه است'})
    return JsonResponse({'success': False, 'error': 'درخواست نامعتبر'})
