from django import forms
from .models import OTP, adviser, Certificate, GENDER_CHOICES, WORK_PREFERENCE_CHOICES, CONSULTATION_METHODS, SPECIALTY_CHOICES, Cafe, Owner, CAFE_TYPES, Podcast
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

    address = forms.CharField(
        label='آدرس دقیق',
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field', 'placeholder': 'آدرس کامل با ذکر محله و پلاک'}),
        required=False
    )

    class Meta:
        model = adviser
        fields = [
            'full_name', 'phone', 'email', 'age', 'gender', 'address', 'location', 'latitude', 'longitude',
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
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 input-field', 'placeholder': 'آدرس کامل با ذکر محله و پلاک'}),
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

class CafeOwnerForm(forms.Form):
    # Cafe fields
    cafe_name = forms.CharField(
        label='نام کافه',
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-amber-500 input-field', 'placeholder': 'نام کامل کافه'})
    )
    cafe_type = forms.ChoiceField(
        label='نوع کافه',
        choices=[('', 'انتخاب کنید')] + list(CAFE_TYPES),
        widget=forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-amber-500 input-field'})
    )
    address = forms.CharField(
        label='آدرس دقیق',
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-amber-500 input-field', 'placeholder': 'آدرس کامل با ذکر محله و پلاک'})
    )
    size = forms.IntegerField(
        label='وسعت کافه (متر مربع)',
        min_value=10,
        widget=forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-amber-500 input-field', 'placeholder': 'مثلا 120'})
    )
    capacity = forms.IntegerField(
        label='ظرفیت (تعداد نفر)',
        min_value=5,
        widget=forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-amber-500 input-field', 'placeholder': 'مثلا 50'})
    )
    menu_file = forms.FileField(
        label='آپلود منوی کافه (PDF یا تصویر)',
        widget=forms.ClearableFileInput(attrs={'id': 'menu-upload'}),
        required=True
    )
    description = forms.CharField(
        label='توضیحات اضافه (اختیاری)',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-amber-500 input-field', 'placeholder': 'توضیحات بیشتر درباره فضای کافه، منوی خاص، جو کافه و...'})
    )
    # Facilities
    has_wifi = forms.BooleanField(label='اینترنت وای فای', required=False)
    has_parking = forms.BooleanField(label='پارکینگ', required=False)
    has_live_music = forms.BooleanField(label='موسیقی زنده', required=False)
    has_outdoor = forms.BooleanField(label='فضای باز', required=False)
    has_hookah = forms.BooleanField(label='قلیان', required=False)
    has_workspace = forms.BooleanField(label='فضای کار', required=False)
    serves_breakfast = forms.BooleanField(label='صبحانه', required=False)
    has_disabled_access = forms.BooleanField(label='دسترسی معلولین', required=False)
    # Owner fields
    owner_full_name = forms.CharField(
        label='نام و نام خانوادگی مالک',
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-amber-500 input-field', 'placeholder': 'نام کامل مالک'})
    )
    owner_national_id = forms.CharField(
        label='کد ملی',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-amber-500 input-field',
            'placeholder': 'کد ملی 10 رقمی',
            'pattern': '\\d{10}',
            'maxlength': '10'
        })
    )
    owner_phone = forms.CharField(
        label='شماره موبایل',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-amber-500 input-field',
            'placeholder': 'مثال: 09123456789',
            'pattern': '09\\d{9}',
            'maxlength': '11'
        })
    )
    owner_email = forms.EmailField(
        label='ایمیل (اختیاری)',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-amber-500 input-field', 'placeholder': 'example@domain.com'})
    )
    accepted_terms = forms.BooleanField(
        label='قوانین و شرایط را قبول دارم',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-amber-600 rounded focus:ring-amber-500 checkbox'})
    )
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)

    def persian_to_english(self, value):
        if not value:
            return ''
        value = str(value)
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        english_digits = '0123456789'
        table = str.maketrans(persian_digits, english_digits)
        return value.translate(table)

    def clean_owner_national_id(self):
        value = self.cleaned_data['owner_national_id']
        value = self.persian_to_english(value)
        if not value.isdigit() or len(value) != 10:
            raise forms.ValidationError('کد ملی باید 10 رقم باشد.')
        return value

    def clean_owner_phone(self):
        value = self.cleaned_data['owner_phone']
        value = self.persian_to_english(value)
        if not value.isdigit() or not value.startswith('09') or len(value) != 11:
            raise forms.ValidationError('شماره موبایل باید با 09 شروع شده و 11 رقم باشد.')
        return value

class PodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ['title', 'category', 'keywords', 'audio_file', 'accepted_rules']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'border border-gray-300 shadow-md rounded-lg px-3 py-2 text-sm', 'placeholder': 'نام عنوان'}),
            'category': forms.Select(attrs={'class': 'border border-gray-300 rounded-lg px-3 py-2 text-sm'}),
            'keywords': forms.TextInput(attrs={'class': 'w-full border border-gray-300 shadow-md rounded-lg px-3 py-2 text-sm', 'placeholder': 'مثلاً: اضطراب، تنهایی، خانواده'}),
            'audio_file': forms.ClearableFileInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 text-sm'}),
            'accepted_rules': forms.CheckboxInput(attrs={'class': 'mt-1 ml-2'}),
        }
        labels = {
            'title': 'عنوان پادکست',
            'category': 'موضوع اصلی',
            'keywords': 'کلمات کلیدی (حداکثر ۳ مورد)',
            'audio_file': 'فایل صوتی',
            'accepted_rules': 'قوانین و مقررات را مطالعه کرده‌ام و می‌پذیرم',
        }

    def clean_keywords(self):
        keywords = self.cleaned_data.get('keywords', '')
        keywords_list = [k.strip() for k in keywords.split(',') if k.strip()]
        if len(keywords_list) > 3:
            raise forms.ValidationError('حداکثر ۳ کلمه کلیدی مجاز است.')
        return ', '.join(keywords_list)

    def clean_accepted_rules(self):
        accepted = self.cleaned_data.get('accepted_rules')
        if not accepted:
            raise forms.ValidationError('پذیرفتن قوانین الزامی است.')
        return accepted