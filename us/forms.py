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
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    specialties = forms.MultipleChoiceField(
        choices=SPECIALTY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    consultation_methods = forms.MultipleChoiceField(
        choices=CONSULTATION_METHODS,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    accepted_terms = forms.BooleanField(
        required=True,
        label='قوانین و شرایط را قبول دارم'
    )

    class Meta:
        model = adviser
        fields = [
            'full_name', 'phone', 'email', 'age', 'gender', 'location',
            'bachelor_field', 'bachelor_year',
            'master_field', 'master_year',
            'phd_field', 'phd_year',
            'is_unemployed', 'current_position', 'current_organization', 'current_description',
            'work_preferences', 'specialties', 'consultation_methods', 'accepted_terms',
        ]

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['file']