from django.db import models

GENDER_CHOICES = [
    ('male', 'مرد'),
    ('female', 'زن'),
]

CONSULTATION_METHODS = [
    ('in_person', 'حضوری'),
    ('online', 'آنلاین'),
    ('phone', 'تلفنی'),
]

WORK_PREFERENCE_CHOICES = [
    ('part_time', 'پاره وقت'),
    ('semi_time', 'نیمه وقت'),
    ('full_time', 'تمام وقت'),
]

SPECIALTY_CHOICES = [
    ('child', 'کودک'),
    ('clinical', 'بالینی'),
    ('family', 'خانواده'),
    ('addiction', 'اعتیاد'),
    ('couple', 'زوج درمانی'),
]

CAFE_TYPES = [
    ('traditional', 'کافه سنتی'),
    ('modern', 'کافه مدرن'),
    ('roastery', 'رستری و تخصصی'),
    ('book', 'کافه کتاب'),
    ('other', 'سایر'),
]

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
    

class adviser(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    phone = models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل')
    email = models.EmailField(unique=True, verbose_name='ایمیل')
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

    is_unemployed = models.BooleanField(default=False)
    current_position = models.CharField(max_length=100, blank=True, null=True, verbose_name='شغل فعلی')
    current_organization = models.CharField(max_length=100, blank=True, null=True, verbose_name='محل کار')
    current_description = models.TextField(blank=True, null=True, verbose_name='توضیحات')

    work_preferences = models.JSONField(default=list, blank=True, verbose_name='مایل به کار')

    specialties = models.JSONField(default=list, verbose_name='زمینه های تخصصی')

    consultation_methods = models.JSONField(default=list, verbose_name='روش های مشاوره')

    accepted_terms = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

class Certificate(models.Model):
    adviser = models.ForeignKey(adviser, on_delete=models.CASCADE, related_name='certificates')
    file = models.FileField(upload_to='certificates/', verbose_name='مدارک')

    def __str__(self):
        return f'Certificate for {self.adviser.full_name}'


class Cafe(models.Model):
    cafe_name = models.CharField(max_length=255, verbose_name='نام کافه')
    cafe_type = models.CharField(max_length=20, choices=CAFE_TYPES, verbose_name='نوع کافه')
    address = models.TextField(verbose_name='آدرس دقیق')
    size = models.PositiveIntegerField(verbose_name='وسعت کافه')
    capacity = models.PositiveIntegerField(verbose_name='ظرفیت')
    menu_file = models.FileField(upload_to='menus/', verbose_name='منو')
    description = models.TextField(blank=True, verbose_name='توضیحات اضافه')
    latitude = models.FloatField(null=True, blank=True, verbose_name='عرض جغرافیایی')
    longitude = models.FloatField(null=True, blank=True, verbose_name='طول جغرافیایی')

    # Facilities
    has_wifi = models.BooleanField(default=False, blank=True)
    has_parking = models.BooleanField(default=False, blank=True)
    has_live_music = models.BooleanField(default=False, blank=True)
    has_outdoor = models.BooleanField(default=False, blank=True)
    has_hookah = models.BooleanField(default=False, blank=True)
    has_workspace = models.BooleanField(default=False, blank=True)
    serves_breakfast = models.BooleanField(default=False, blank=True)
    has_disabled_access = models.BooleanField(default=False, blank=True)
    accepted_terms = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.cafe_name


class Owner(models.Model):
    cafe = models.OneToOneField(Cafe, on_delete=models.CASCADE, related_name='owner')
    full_name = models.CharField(max_length=255, verbose_name='نام و نام خانوادگی مالک')
    national_id = models.CharField(max_length=10, verbose_name='کد ملی')
    phone = models.CharField(max_length=11, verbose_name='شماره موبایل')
    email = models.EmailField(blank=True, verbose_name='ایمیل')

    def __str__(self):
        return self.full_name


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

    def __str__(self):
        return self.title


