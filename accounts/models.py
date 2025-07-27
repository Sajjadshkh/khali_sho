from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='شماره تلفن')
    bio = models.TextField(blank=True, null=True)

class Testimonial(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کاربر مرتبط")
    name = models.CharField(max_length=100, verbose_name="نام")
    position = models.CharField(max_length=100, verbose_name="سمت")
    experience = models.TextField(verbose_name="تجربه")
    is_active = models.BooleanField(default=False, verbose_name="نمایش در سایت")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "نظر کاربر"
        verbose_name_plural = "نظرات کاربران"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.position}"