from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, View
from django.urls import reverse_lazy, reverse
from uuid import uuid4
from datetime import datetime, timedelta
from .models import Aboutus, OTP, adviser, Certificate, Cafe, Owner
from .forms import OTPForm, CheckOTPForm, AdviserForm, CertificateForm, CafeOwnerForm, PodcastForm
from random import randint
import ghasedakpack
from django.contrib import messages


SMS = ghasedakpack.Ghasedak(
    "3f37ee30f4690b3334c5e3552b67615a4171d8a1f2ed7444efb87b628bd53e9b")

class AboutUsView(ListView):
    template_name = 'us/aboutus.html'
    model = Aboutus
    context_object_name = 'aboutus'

class ServicesView(ListView):
    template_name = 'us/services.html'
    model = Aboutus
    context_object_name = 'aboutus'

class PodcastsView(ListView):
    template_name = 'us/podcasts.html'
    model = Aboutus
    context_object_name = 'aboutus'


def podcast_create(request):
    if request.method == 'POST':
        form = PodcastForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'پادکست شما با موفقیت ثبت شد و پس از بررسی منتشر خواهد شد.')
            return redirect('us:podcast_create')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را برطرف کنید.')
    else:
        form = PodcastForm()
    return render(request, 'us/podcast_create.html', {'form': form})



class AdviserCreateView(CreateView):
    model = adviser
    form_class = AdviserForm
    template_name = 'us/workusadviser.html'
    success_url = reverse_lazy('home:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        files = self.request.FILES.getlist('certificates')
        for f in files:
            Certificate.objects.create(adviser=self.object, file=f)
        return response

class CafeCreateView(View):
    template_name = 'us/workuscafe.html'
    success_url = reverse_lazy('home:home')

    def get(self, request):
        form = CafeOwnerForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CafeOwnerForm(request.POST, request.FILES)
        if form.is_valid():
            # ذخیره Cafe
            cafe = Cafe.objects.create(
                cafe_name=form.cleaned_data['cafe_name'],
                cafe_type=form.cleaned_data['cafe_type'],
                address=form.cleaned_data['address'],
                size=form.cleaned_data['size'],
                capacity=form.cleaned_data['capacity'],
                menu_file=form.cleaned_data['menu_file'],
                description=form.cleaned_data['description'],
                has_wifi=form.cleaned_data['has_wifi'],
                has_parking=form.cleaned_data['has_parking'],
                has_live_music=form.cleaned_data['has_live_music'],
                has_outdoor=form.cleaned_data['has_outdoor'],
                has_hookah=form.cleaned_data['has_hookah'],
                has_workspace=form.cleaned_data['has_workspace'],
                serves_breakfast=form.cleaned_data['serves_breakfast'],
                has_disabled_access=form.cleaned_data['has_disabled_access'],
                accepted_terms=form.cleaned_data['accepted_terms'],
                latitude=form.cleaned_data.get('latitude'),
                longitude=form.cleaned_data.get('longitude'),
            )
            # ذخیره Owner
            Owner.objects.create(
                cafe=cafe,
                full_name=form.cleaned_data['owner_full_name'],
                national_id=form.cleaned_data['owner_national_id'],
                phone=form.cleaned_data['owner_phone'],
                email=form.cleaned_data['owner_email'],
            )
            return redirect(self.success_url)
        # اگر فرم نامعتبر بود، همان صفحه با خطاها نمایش داده شود
        return render(request, self.template_name, {'form': form})


class OTPView(View):
   
   def get(self, request):
        # template_name = 'us/otp.html'
        form = OTPForm()
        return render(request, 'us/otp.html', {'form': form})
   
   def post(self, request):
    form = OTPForm(request.POST)
    # اگر فرم اصلی ارسال شده بود
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
        # ذخیره شماره تلفن در session
        request.session['otp_phone'] = cd['phone']
        # گرفتن پارامتر next از URL یا استفاده از مسیر پیش‌فرض
        next_url = request.GET.get('next', reverse('accounts:register'))
        return redirect(f"{reverse('us:checkotp')}?token={token}&next={next_url}")
    # اگر فرم اصلی نبود و درخواست ارسال مجدد بود
    elif 'otp_phone' in request.session:
        phone = request.session['otp_phone']
        randcode = randint(1000, 9999)
        SMS.verification(
            {'receptor': phone, 'type': '1',
             'template': 'randcode', 'param1': randcode}
        )
        token = str(uuid4())
        OTP.objects.create(phone=phone, code=randcode, token=token)
        print(randcode)
        # گرفتن پارامتر next از URL یا استفاده از مسیر پیش‌فرض
        next_url = request.GET.get('next', reverse('accounts:register'))
        return redirect(f"{reverse('us:checkotp')}?token={token}&next={next_url}")
    else:
        form.add_error("phone", "invalid data")

    return render(request, 'us/otp.html', {'form': form})
   

class CheckOTPView(View):

    def get(self, request):
        form = CheckOTPForm()
        return render(request, 'us/checkotp.html', {'form': form})
    
    def post(self, request):
        token = request.GET.get('token')
        next_url = request.GET.get('next', reverse('accounts:register'))  # fallback
        form = CheckOTPForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            if OTP.objects.filter(code=cd['code'], token=token).exists():
                otp = OTP.objects.get(token=token)
                otp.delete()
            # ✅ ذخیره تأیید OTP در session
                request.session['otp_verified'] = True
                # در CheckOTPView بعد از تایید موفق
                request.session["otp_verified_time"] = datetime.now().timestamp()
                return redirect(next_url)
            else:
                form.add_error("code", "کد نادرست است")
        else:
            form.add_error("code", "داده وارد شده نامعتبر است")

            return render(request, 'us/checkotp.html', {'form': form})