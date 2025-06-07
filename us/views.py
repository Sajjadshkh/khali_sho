from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, View
from django.urls import reverse_lazy, reverse
from uuid import uuid4
from .models import Aboutus, OTP
from .forms import OTPForm, CheckOTPForm
from random import randint
import ghasedakpack


SMS = ghasedakpack.Ghasedak(
    "3f37ee30f4690b3334c5e3552b67615a4171d8a1f2ed7444efb87b628bd53e9b")

class AboutUsView(ListView):
    template_name = 'us/aboutus.html'
    model = Aboutus
    context_object_name = 'aboutus'

class PodcastsView(ListView):
    template_name = 'us/podcasts.html'
    model = Aboutus
    context_object_name = 'aboutus'


class PodcastCreateView(ListView):
    model = Aboutus
    # form_class = PodcastForm
    template_name = 'us/podcast_create.html'
    success_url = reverse_lazy('us:podcasts')


class OTPView(View):

    def get(self, request):
        template_name = 'us/otp.html'
        form = OTPForm()
        return render(request, 'us/otp.html', {'form': form})

    def post(self, request):
        form = OTPForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)
            SMS.verification(
                {'receptor': cd["phone"], 'type': '1',
                 'template': 'randcode', 'param1': randcode}
            )
            token = str(uuid4())
            OTP.objects.create(phone=cd['phone'], code=randcode, token=token)
            print(randcode)
            return redirect(reverse('us:checkotp') + f"?token={token}")

        else:
            form.add_error("phone", "invalid data")

        return render(request, 'us/otp.html', {'form': form})


class CheckOTPView(View):
    def get(self, request):
        template_name = 'us/checkotp.html'
        form = CheckOTPForm()
        return render(request, 'us/checkotp.html', {'form': form})

    def post(self, request):
        token = request.GET.get('token')
        form = CheckOTPForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if OTP.objects.filter(code=cd['code'], token=token).exists():
                otp = OTP.objects.get(token=token)
                otp.delete()
                return redirect('us:podcast_create')

        else:
            form.add_error("code", "invalid data")

        return render(request, 'us/checkotp.html', {'form': form})