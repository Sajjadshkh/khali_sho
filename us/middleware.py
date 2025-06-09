from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime, timedelta

class OTPVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = [
            reverse('us:podcast_create'),
            reverse('accounts:register'),
            # مسیرهای بیشتری اضافه کن اگر خواستی
        ]

        if request.path in protected_paths:
            otp_verified = request.session.get('otp_verified', False)
            otp_time = request.session.get('otp_verified_time')

            # اگر اصلاً otp_verified نیست یا زمانش منقضی شده
            if not otp_verified or not otp_time:
                return self.redirect_to_otp(request)

            # بررسی زمان انقضا (مثلاً ۵ دقیقه)
            verified_time = datetime.fromtimestamp(otp_time)
            if datetime.now() - verified_time > timedelta(minutes=15):
                # پاک کردن وضعیت OTP منقضی‌شده
                request.session.pop('otp_verified', None)
                request.session.pop('otp_verified_time', None)
                return self.redirect_to_otp(request)

        return self.get_response(request)

    def redirect_to_otp(self, request):
        otp_url = reverse('us:otp')
        return redirect(f"{otp_url}?next={request.path}")