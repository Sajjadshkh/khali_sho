from django.db import models

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
    
class Cafe(models.Model):
    CAFE_TYPES = [
        ('traditional', 'کافه سنتی'),
        ('modern', 'کافه مدرن'),
        ('roastery', 'رستری و تخصصی'),
        ('book', 'کافه کتاب'),
        ('other', 'سایر'),
    ]

    name = models.CharField(max_length=255)
    cafe_type = models.CharField(max_length=20, choices=CAFE_TYPES)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    size = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    menu_file = models.FileField(upload_to='menus/')
    description = models.TextField(blank=True)

    # Facilities
    has_wifi = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_live_music = models.BooleanField(default=False)
    has_outdoor = models.BooleanField(default=False)
    has_hookah = models.BooleanField(default=False)
    has_workspace = models.BooleanField(default=False)
    serves_breakfast = models.BooleanField(default=False)
    has_disabled_access = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Owner(models.Model):
    cafe = models.OneToOneField(Cafe, on_delete=models.CASCADE, related_name='owner')
    full_name = models.CharField(max_length=255)
    national_id = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.full_name