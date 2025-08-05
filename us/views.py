from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, View
from django.urls import reverse_lazy, reverse
from uuid import uuid4
from datetime import datetime, timedelta
from .models import Aboutus, OTP, Adviser, Certificate, Cafe, Owner, Podcast, Plan, Cart, CartItem, Order, OrderItem, Donation
from .forms import OTPForm, CheckOTPForm, AdviserForm, CertificateForm, CafeOwnerForm, PodcastForm, DonationForm
from random import randint
import ghasedakpack
from django.contrib import messages
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests
import json


SMS = ghasedakpack.Ghasedak(
    "3f37ee30f4690b3334c5e3552b67615a4171d8a1f2ed7444efb87b628bd53e9b")



class ServicesView(ListView):
    template_name = 'us/services.html'
    model = Aboutus
    context_object_name = 'aboutus'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # اضافه کردن پلن‌های فعال
        context['phone_plans'] = Plan.objects.filter(plan_type='phone', is_active=True).order_by('price')
        context['inperson_plans'] = Plan.objects.filter(plan_type='inperson', is_active=True).order_by('price')
        return context

class PodcastsView(ListView):
    template_name = 'us/podcasts.html'
    model = Podcast
    context_object_name = 'podcasts'

    def get_queryset(self):
        queryset = Podcast.objects.filter(is_approved=True).order_by('-created_at')
        category = self.request.GET.get('category')
        if category and category != 'همه موضوعات':
            queryset = queryset.filter(category=category)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(keywords__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Podcast.CATEGORY_CHOICES 
        context['selected_category'] = self.request.GET.get('category', '')
        context['request'] = self.request
        return context


def podcast_create(request):
    if request.method == 'POST':
        form = PodcastForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'پادکست شما با موفقیت ثبت شد و پس از بررسی منتشر خواهد شد.',
                extra_tags='podcast'
            )
            return redirect('us:podcast_create')
        else:
            messages.error(
                request,
                'لطفاً خطاهای فرم را برطرف کنید.',
                extra_tags='podcast'
            )
    else:
        form = PodcastForm()
    return render(request, 'us/podcast_create.html', {'form': form})



class AdviserCreateView(CreateView):
    model = Adviser
    form_class = AdviserForm
    template_name = 'us/workusadviser.html'
    success_url = reverse_lazy('home:home')

    def get_initial(self):
        initial = super().get_initial()
        initial['phone'] = self.request.session.get('otp_phone', '')
        return initial

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

class AllAdvisersView(ListView):
    model = Adviser
    template_name = 'us/aboutus.html'
    context_object_name = 'advisers_list'

    def get_queryset(self):
        return Adviser.objects.filter(is_approved=True).order_by('-created_at')
class AboutUsView(ListView):
    template_name = 'us/aboutus.html'
    model = Aboutus
    context_object_name = 'aboutus'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advisers_list'] = Adviser.objects.filter(is_approved=True)
        context['featured_cafes'] = Cafe.objects.filter(is_featured=True)[:8]
        return context

class CafeCreateView(View):
    template_name = 'us/workuscafe.html'
    success_url = reverse_lazy('home:home')

    def get(self, request):
        initial = {'owner_phone': request.session.get('otp_phone', '')}
        form = CafeOwnerForm(initial=initial)
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
                image=form.cleaned_data.get('image'),
                description=form.cleaned_data['description'],
                has_parking=form.cleaned_data['has_parking'],
                has_workspace=form.cleaned_data['has_workspace'],
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

# View های جدید برای سیستم خرید
def get_or_create_cart(request):
    """دریافت یا ایجاد سبد خرید برای کاربر"""
    if not request.session.session_key:
        request.session.create()
    
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

def add_to_cart(request, plan_id):
    """اضافه کردن پلن به سبد خرید"""
    if request.method == 'POST':
        plan = get_object_or_404(Plan, id=plan_id, is_active=True)
        cart = get_or_create_cart(request)
        
        # بررسی اینکه آیا این پلن قبلاً در سبد خرید وجود دارد
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            plan=plan,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        messages.success(request, f'پلن {plan.name} به سبد خرید اضافه شد.')
        return redirect('us:cart')
    
    return redirect('us:services')

def cart_view(request):
    """نمایش سبد خرید"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.get_total_price(),
    }
    return render(request, 'us/cart.html', context)

def remove_from_cart(request, item_id):
    """حذف آیتم از سبد خرید"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__session_key=request.session.session_key)
    cart_item.delete()
    messages.success(request, 'آیتم از سبد خرید حذف شد.')
    return redirect('us:cart')

def update_cart_item(request, item_id):
    """بروزرسانی تعداد آیتم در سبد خرید"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, id=item_id, cart__session_key=request.session.session_key)
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'total_price': cart_item.cart.get_total_price(),
            'item_total': cart_item.get_total_price()
        })
    
    return JsonResponse({'success': False})

def checkout_view(request):
    """صفحه تسویه حساب"""
    # بررسی لاگین
    if not request.user.is_authenticated:
        return redirect(f"{reverse('accounts:login')}?next={reverse('us:checkout')}")
    
    # اگر کاربر لاگین است، OTP نمی‌خواهیم
    # OTP فقط برای کاربران مهمان است
    # if not request.session.get('otp_verified'):
    #     messages.error(request, 'لطفاً ابتدا شماره تلفن خود را تایید کنید.')
    #     return redirect(f"{reverse('us:otp')}?next={reverse('us:checkout')}")
    
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.error(request, 'سبد خرید شما خالی است.')
        return redirect('us:services')
    
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if phone:
            # ایجاد سفارش
            order = Order.objects.create(
                user=request.user,  # اضافه کردن کاربر
                phone=phone,
                total_amount=cart.get_total_price()
            )
            
            # انتقال آیتم‌ها از سبد خرید به سفارش
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    plan=cart_item.plan,
                    quantity=cart_item.quantity,
                    price=cart_item.plan.price,
                    total_price=cart_item.get_total_price()
                )
            
            # پاک کردن سبد خرید
            cart.delete()
            
            # انتقال به صفحه پرداخت
            return redirect('us:payment', order_id=order.id)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.get_total_price(),
    }
    return render(request, 'us/checkout.html', context)

def payment_view(request, order_id):
    """صفحه پرداخت"""
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # اینجا کد اتصال به درگاه شاپرک قرار می‌گیرد
        payment_result = process_shaparak_payment(order)
        
        if payment_result['success']:
            order.status = 'paid'
            order.payment_id = payment_result['payment_id']
            order.save()
            messages.success(request, 'پرداخت با موفقیت انجام شد.')
            return redirect('us:order_success', order_id=order.id)
        else:
            order.status = 'failed'
            order.save()
            messages.error(request, 'پرداخت ناموفق بود. لطفاً دوباره تلاش کنید.')
            return redirect('us:payment', order_id=order.id)
    
    context = {
        'order': order,
        'order_items': order.items.all(),
    }
    return render(request, 'us/payment.html', context)

from .shaparak import process_shaparak_payment

@method_decorator(csrf_exempt, name='dispatch')
class PaymentCallbackView(View):
    """دریافت callback از درگاه پرداخت"""
    
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        
        # بررسی وضعیت پرداخت از درگاه
        payment_status = request.POST.get('status')
        payment_id = request.POST.get('payment_id')
        
        if payment_status == 'success':
            order.status = 'paid'
            order.payment_id = payment_id
            order.save()
            return JsonResponse({'status': 'success'})
        else:
            order.status = 'failed'
            order.save()
            return JsonResponse({'status': 'failed'})

def order_success(request, order_id):
    """صفحه موفقیت پرداخت"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'us/order_success.html', {'order': order})

def order_detail(request, order_id):
    """جزئیات سفارش"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'us/order_detail.html', {'order': order})

def get_cart_count(request):
    """دریافت تعداد آیتم‌های سبد خرید"""
    if request.session.session_key:
        try:
            cart = Cart.objects.get(session_key=request.session.session_key)
            return cart.items.count()
        except Cart.DoesNotExist:
            return 0
    return 0

# Views مربوط به سیستم حمایت مالی
def donation_view(request):
    """صفحه فرم حمایت مالی"""
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.save()
            messages.success(request, 'اطلاعات حمایت شما ثبت شد. لطفاً برای تکمیل فرآیند پرداخت اقدام کنید.')
            return redirect('us:donation_payment', donation_id=donation.id)
        else:
            messages.error(request, 'لطفاً خطاهای فرم را برطرف کنید.')
    else:
        form = DonationForm()
    
    context = {
        'form': form,
        'donation_types': Donation.DONATION_TYPES,
    }
    return render(request, 'us/donation.html', context)

def donation_payment_view(request, donation_id):
    """صفحه پرداخت حمایت مالی"""
    donation = get_object_or_404(Donation, id=donation_id)
    
    if request.method == 'POST':
        # اینجا کد اتصال به درگاه شاپرک قرار می‌گیرد
        payment_result = process_shaparak_payment_donation(donation)
        
        if payment_result['success']:
            donation.status = 'completed'
            donation.payment_id = payment_result['payment_id']
            donation.save()
            messages.success(request, 'حمایت شما با موفقیت ثبت شد. از همراهی شما سپاسگزاریم.')
            return redirect('us:donation_success', donation_id=donation.id)
        else:
            donation.status = 'failed'
            donation.save()
            messages.error(request, 'پرداخت ناموفق بود. لطفاً دوباره تلاش کنید.')
            return redirect('us:donation_payment', donation_id=donation.id)
    
    context = {
        'donation': donation,
    }
    return render(request, 'us/donation_payment.html', context)

@method_decorator(csrf_exempt, name='dispatch')
class DonationPaymentCallbackView(View):
    """دریافت callback از درگاه پرداخت برای حمایت مالی"""
    
    def post(self, request, donation_id):
        donation = get_object_or_404(Donation, id=donation_id)
        
        # بررسی وضعیت پرداخت از درگاه
        payment_status = request.POST.get('status')
        payment_id = request.POST.get('payment_id')
        
        if payment_status == 'success':
            donation.status = 'completed'
            donation.payment_id = payment_id
            donation.save()
            return JsonResponse({'status': 'success'})
        else:
            donation.status = 'failed'
            donation.save()
            return JsonResponse({'status': 'failed'})

def donation_success(request, donation_id):
    """صفحه موفقیت حمایت مالی"""
    donation = get_object_or_404(Donation, id=donation_id)
    return render(request, 'us/donation_success.html', {'donation': donation})

def donation_list(request):
    """لیست حمایت‌های مالی (برای ادمین)"""
    donations = Donation.objects.filter(status='completed').order_by('-created_at')
    total_amount = sum(donation.amount for donation in donations)
    
    context = {
        'donations': donations,
        'total_amount': total_amount,
    }
    return render(request, 'us/donation_list.html', context)

# تابع کمکی برای پرداخت حمایت مالی
def process_shaparak_payment_donation(donation):
    """پردازش پرداخت حمایت مالی از طریق درگاه شاپرک"""
    # این تابع مشابه process_shaparak_payment است اما برای حمایت مالی
    # در اینجا کد اتصال به درگاه پرداخت قرار می‌گیرد
    return {
        'success': True,
        'payment_id': f'donation_{donation.id}_{uuid4().hex[:8]}'
    }