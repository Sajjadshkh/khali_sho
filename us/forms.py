from django import forms
from .models import OTP, adviser, Certificate, GENDER_CHOICES, WORK_PREFERENCE_CHOICES, CONSULTATION_METHODS, SPECIALTY_CHOICES
from django.core import validators

class OTPForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), validators=[validators.MaxLengthValidator(11)])


class CheckOTPForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), validators=[validators.MaxLengthValidator(4)])
    
    
class AdviserForm(forms.ModelForm):
    work_preferences = forms.MultipleChoiceField(
        choices=WORK_PREFERENCE_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'w-4 h-4 text-indigo-600 rounded focus:ring-indigo-500 checkbox'}),
        required=False
    )

    specialties = forms.MultipleChoiceField(
        choices=SPECIALTY_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'w-4 h-4 text-indigo-600 rounded focus:ring-indigo-500 checkbox'}),
        required=True
    )

    consultation_methods = forms.MultipleChoiceField(
        choices=CONSULTATION_METHODS,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'w-4 h-4 text-indigo-600 rounded focus:ring-indigo-500 checkbox'}),
        required=True
    )

    accepted_terms = forms.BooleanField(
        required=True,
        label='قوانین و شرایط را قبول دارم',
        widget=forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-indigo-600 rounded focus:ring-indigo-500 checkbox'})
    )

    class Meta:
        model = adviser
        fields = [
            'full_name', 'phone', 'email', 'age', 'gender', 'location', 'latitude', 'longitude',
            'bachelor_field', 'bachelor_year',
            'master_field', 'master_year',
            'phd_field', 'phd_year',
            'is_unemployed', 'current_position', 'current_organization', 'current_description',
            'work_preferences', 'specialties', 'consultation_methods', 'accepted_terms',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field',
                'placeholder': 'نام کامل'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field',
                'placeholder': 'مثال: 09123456789',
                'pattern': '09\\d{9}',
                'maxlength': '11'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field',
                'placeholder': 'example@domain.com'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field',
                'placeholder': 'سن شما',
                'min': '22',
                'max': '80'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field',
                'placeholder': 'موقعیت خود را وارد کنید'
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'bachelor_field': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field',
                'placeholder': 'مثال: روانشناسی بالینی'
            }),
            'bachelor_year': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field',
                'placeholder': 'مثال: 1395',
                'min': '1350',
                'max': '1405'
            }),
            'master_field': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field',
                'placeholder': 'مثال: روانشناسی خانواده'
            }),
            'master_year': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field',
                'placeholder': 'مثال: 1398',
                'min': '1350',
                'max': '1405'
            }),
            'phd_field': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field',
                'placeholder': 'مثال: روانشناسی کودک'
            }),
            'phd_year': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field',
                'placeholder': 'مثال: 1400',
                'min': '1350',
                'max': '1405'
            }),
            'is_unemployed': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-indigo-600 rounded focus:ring-indigo-500 checkbox'
            }),
            'current_position': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field',
                'placeholder': 'مثال: روانشناس کودک'
            }),
            'current_organization': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field',
                'placeholder': 'نام کلینیک یا مرکز'
            }),
            'current_description': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field',
                'placeholder': 'توضیحات بیشتر'
            }),
        }

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['file']