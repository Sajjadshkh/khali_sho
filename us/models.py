from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

GENDER_CHOICES = [
    ('male', 'مرد'),
    ('female', 'زن'),
]

CONSULTATION_METHODS = [
    ('حضوری', 'حضوری'),
    ('آنلاین', 'آنلاین'),
    ('تلفنی', 'تلفنی'),
]

WORK_PREFERENCE_CHOICES = [
    ('پاره وقت', 'پاره وقت'),
    ('نیمه وقت', 'نیمه وقت'),
    ('تمام وقت', 'تمام وقت'),
]

SPECIALTY_CHOICES = [
    ('کودک', 'کودک'),
    ('بالینی', 'بالینی'),
    ('خانواده', 'خانواده'),
    ('اعتیاد', 'اعتیاد'),
    ('زوج درمانی', 'زوج درمانی'),
    ('مشاوره طلاق', 'مشاوره طلاق'),
    ('منابع انسانی', 'منابع انسانی'),
    ('حقوقی', 'حقوقی'),
    ('تربیتی', 'تربیتی'),
    ('اعتیاد', 'اعتیاد'),
]

CAFE_TYPES = [
    ('traditional restaurant', 'رستوران سنتی'),
    ('cafe', 'کافه'),
    ('cafe restaurant', 'کافه رستوران'),
    ('book cafe', 'کافه کتاب'),
    ('other', 'سایر'),
]

# مدل‌های جدید برای سیستم خرید
class Plan(models.Model):
    PLAN_TYPES = [
        ('phone', 'تلفنی'),
        ('inperson', 'حضوری'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='نام پلن')
    plan_type = models.CharField(max_length=10, choices=PLAN_TYPES, verbose_name='نوع پلن')
    duration = models.IntegerField(verbose_name='مدت زمان (دقیقه)')
    extra_time = models.IntegerField(verbose_name='زمان اضافه (دقیقه)')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='قیمت (تومان)')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_plan_type_display()}"
    
    class Meta:
        verbose_name = "پلن"
        verbose_name_plural = "پلن‌ها"

class Cart(models.Model):
    session_key = models.CharField(max_length=40, unique=True, verbose_name='کلید نشست')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"سبد خرید {self.session_key}"
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='سبد خرید')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name='پلن')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.plan.name} - {self.quantity}"
    
    def get_total_price(self):
        return self.plan.price * self.quantity
    
    class Meta:
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم‌های سبد خرید"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('cancelled', 'لغو شده'),
        ('failed', 'ناموفق'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', null=True, blank=True)
    order_number = models.CharField(max_length=20, unique=True, verbose_name='شماره سفارش')
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن')
    total_amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='مبلغ کل')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    payment_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='شناسه پرداخت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    def __str__(self):
        return f"سفارش {self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # تولید شماره سفارش منحصر به فرد
            import random
            import string
            while True:
                order_number = ''.join(random.choices(string.digits, k=8))
                if not Order.objects.filter(order_number=order_number).exists():
                    self.order_number = order_number
                    break
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name='پلن')
    quantity = models.PositiveIntegerField(verbose_name='تعداد')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='قیمت واحد')
    total_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='قیمت کل')
    
    def __str__(self):
        return f"{self.plan.name} - {self.quantity}"
    
    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"


class Aboutus(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(verbose_name='عکس')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "درباره ما"
        verbose_name_plural = "درباره ما"


class OTP(models.Model):
    token = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    expration_code = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone
    

class Adviser(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    phone = models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل')
    image = models.ImageField(upload_to='advisers/', verbose_name='عکس', blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name='ایمیل', blank=True, null=True)
    age = models.PositiveIntegerField(verbose_name='سن')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='جنسیت')
    location = models.CharField(max_length=255, verbose_name='موقعیت', blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True, verbose_name='عرض جغرافیایی')
    longitude = models.FloatField(null=True, blank=True, verbose_name='طول جغرافیایی')
    address = models.TextField(verbose_name='آدرس دقیق', blank=True, null=True)

    bachelor_field = models.CharField(max_length=100, verbose_name='رشته تحصیلی کارشناسی')
    bachelor_year = models.PositiveIntegerField(verbose_name='سال فارغ التحصیلی کارشناسی')
    master_field = models.CharField(max_length=100, blank=True, null=True, verbose_name='رشته تحصیلی کارشناسی ارشد')
    master_year = models.PositiveIntegerField(blank=True, null=True, verbose_name='سال فارغ التحصیلی کارشناسی ارشد')
    phd_field = models.CharField(max_length=100, blank=True, null=True, verbose_name='رشته تحصیلی دکتری')
    phd_year = models.PositiveIntegerField(blank=True, null=True, verbose_name='سال فارغ التحصیلی دکتری')

    is_unemployed = models.BooleanField(default=False, verbose_name='آیا در حال حاضر مشغول به کار هستید؟')
    current_position = models.CharField(max_length=100, blank=True, null=True, verbose_name='شغل فعلی')
    current_organization = models.CharField(max_length=100, blank=True, null=True, verbose_name='محل کار')
    current_description = models.TextField(blank=True, null=True, verbose_name='توضیحات شغلی')

    work_preferences = models.JSONField(default=list, blank=True, verbose_name='مایل به کار')

    specialties = models.JSONField(default=list, verbose_name='زمینه های تخصصی')

    consultation_methods = models.JSONField(default=list, verbose_name='روش های مشاوره')

    accepted_terms = models.BooleanField(default=False, verbose_name='قوانین و مقررات را قبول دارم')
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده توسط ادمین")
    is_featured = models.BooleanField(default=False, verbose_name='نمایش به عنوان مشاور برتر')

    def __str__(self):
        return self.full_name
    class Meta:
        verbose_name = "مشاور"
        verbose_name_plural = "مشاوران"

class Certificate(models.Model):
    adviser = models.ForeignKey(Adviser, on_delete=models.CASCADE, related_name='certificates')
    file = models.FileField(upload_to='certificates/', verbose_name='مدارک')

    def __str__(self):
        return f'Certificate for {self.adviser.full_name}'
    class Meta:
        verbose_name = "مدرک"
        verbose_name_plural = "مدرک‌ها"


class Cafe(models.Model):
    cafe_name = models.CharField(max_length=255, verbose_name='نام کافه')
    cafe_type = models.CharField(max_length=30, choices=CAFE_TYPES, verbose_name='نوع کافه')
    address = models.TextField(verbose_name='آدرس دقیق')
    size = models.PositiveIntegerField(verbose_name='وسعت کافه')
    capacity = models.PositiveIntegerField(verbose_name='ظرفیت')
    menu_file = models.FileField(blank=True, null=True, upload_to='menus/', verbose_name='منو')
    description = models.TextField(blank=True, verbose_name='توضیحات اضافه')
    latitude = models.FloatField(null=True, blank=True, verbose_name='عرض جغرافیایی')
    longitude = models.FloatField(null=True, blank=True, verbose_name='طول جغرافیایی')
    image = models.ImageField(upload_to='cafes/', verbose_name='لوگوی کافه', blank=True, null=True)

    # Facilities
    has_parking = models.BooleanField(default=False, blank=True, verbose_name='پارکینگ')
    has_workspace = models.BooleanField(default=False, blank=True, verbose_name='فضای کار')
    has_disabled_access = models.BooleanField(default=False, blank=True, verbose_name='دسترسی معلولین')
    accepted_terms = models.BooleanField(default=False, blank=True, verbose_name='قوانین و مقررات را قبول دارم')
    is_featured = models.BooleanField(default=False, verbose_name='نمایش در صفحه درباره ما')

    def __str__(self):
        return self.cafe_name
    class Meta:
        verbose_name = "کافه"
        verbose_name_plural = "کافه‌ها"


class Owner(models.Model):
    cafe = models.OneToOneField(Cafe, on_delete=models.CASCADE, related_name='owner')
    full_name = models.CharField(max_length=255, verbose_name='نام و نام خانوادگی مالک')
    national_id = models.CharField(max_length=10, verbose_name='کد ملی')
    phone = models.CharField(max_length=11, verbose_name='شماره موبایل')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')

    def __str__(self):
        return self.full_name
    class Meta:
        verbose_name = "مالک"
        verbose_name_plural = "مالکان"

class Podcast(models.Model):
    CATEGORY_CHOICES = [
        ("روابط عاطفی", "روابط عاطفی"),
        ("خانواده", "خانواده"),
        ("اضطراب و استرس", "اضطراب و استرس"),
        ("افسردگی", "افسردگی"),
        ("مسائل شغلی", "مسائل شغلی"),
        ("بحران‌های روانی", "بحران‌های روانی"),
        ("سایر", "سایر"),
    ]
    title = models.CharField(max_length=200, verbose_name="عنوان پادکست")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="موضوع اصلی")
    keywords = models.CharField(max_length=100, verbose_name="کلمات کلیدی")
    audio_file = models.FileField(upload_to="podcasts/", verbose_name="فایل صوتی")
    accepted_rules = models.BooleanField(verbose_name="تایید قوانین")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده توسط ادمین")

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "پادکست"
        verbose_name_plural = "پادکست‌ها"    


class Donation(models.Model):
    DONATION_TYPES = [
        ('charity', 'خیریه'),
        ('support', 'حمایت از پروژه'),
        ('general', 'حمایت عمومی'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('completed', 'پرداخت شده'),
        ('failed', 'ناموفق'),
        ('cancelled', 'لغو شده'),
    ]
    
    donor_name = models.CharField(max_length=100, verbose_name='نام اهداکننده', blank=True, null=True)
    donor_phone = models.CharField(max_length=11, verbose_name='شماره تلفن')
    donor_email = models.EmailField(verbose_name='ایمیل', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='مبلغ (تومان)')
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPES, default='charity', verbose_name='نوع حمایت')
    message = models.TextField(verbose_name='پیام', blank=True, null=True)
    is_anonymous = models.BooleanField(default=False, verbose_name='حمایت ناشناس')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    payment_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='شناسه پرداخت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    def __str__(self):
        return f"حمایت {self.amount} تومانی - {self.get_donation_type_display()}"
    
    class Meta:
        verbose_name = "حمایت مالی"
        verbose_name_plural = "حمایت‌های مالی"
        ordering = ['-created_at']    


