// تبدیل اعداد فارسی به انگلیسی
function convertPersianToEnglish(input) {
    const persianNumbers = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    const englishNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    
    let result = input;
    for (let i = 0; i < persianNumbers.length; i++) {
        result = result.replace(new RegExp(persianNumbers[i], 'g'), englishNumbers[i]);
    }
    return result;
}

// محدودیت شماره تلفن به 11 رقم
function limitPhoneNumber(input) {
    // حذف کاراکترهای غیر عددی
    let value = input.value.replace(/\D/g, '');
    
    // محدودیت به 11 رقم
    if (value.length > 11) {
        value = value.substring(0, 11);
    }
    
    // اگر با 09 شروع نشود، حذف کن
    if (value.length > 0 && !value.startsWith('09')) {
        value = '';
    }
    
    input.value = value;
}

// محدودیت کد OTP به 4 رقم
function limitOTPCode(input) {
    // حذف کاراکترهای غیر عددی
    let value = input.value.replace(/\D/g, '');
    
    // محدودیت به 4 رقم
    if (value.length > 4) {
        value = value.substring(0, 4);
    }
    
    input.value = value;
}

// اعمال محدودیت‌ها روی فیلدهای شماره تلفن
document.addEventListener('DOMContentLoaded', function() {
    console.log('Phone input script loaded successfully!');
    // فیلدهای شماره تلفن
    const phoneInputs = document.querySelectorAll('input[type="tel"], input[name="phone"], input[name="mobile"]');
    console.log('Found phone inputs:', phoneInputs.length);
    
    phoneInputs.forEach(function(input) {
        // تبدیل اعداد فارسی به انگلیسی هنگام تایپ
        input.addEventListener('input', function() {
            this.value = convertPersianToEnglish(this.value);
            limitPhoneNumber(this);
        });
        
        // تبدیل اعداد فارسی به انگلیسی هنگام paste
        input.addEventListener('paste', function(e) {
            setTimeout(() => {
                this.value = convertPersianToEnglish(this.value);
                limitPhoneNumber(this);
            }, 0);
        });
        
        // تبدیل اعداد فارسی به انگلیسی هنگام drop
        input.addEventListener('drop', function(e) {
            setTimeout(() => {
                this.value = convertPersianToEnglish(this.value);
                limitPhoneNumber(this);
            }, 0);
        });
    });
    
    // فیلدهای کد OTP
    const otpInputs = document.querySelectorAll('input[name="code"]');
    
    otpInputs.forEach(function(input) {
        // تبدیل اعداد فارسی به انگلیسی هنگام تایپ
        input.addEventListener('input', function() {
            this.value = convertPersianToEnglish(this.value);
            limitOTPCode(this);
        });
        
        // تبدیل اعداد فارسی به انگلیسی هنگام paste
        input.addEventListener('paste', function(e) {
            setTimeout(() => {
                this.value = convertPersianToEnglish(this.value);
                limitOTPCode(this);
            }, 0);
        });
        
        // تبدیل اعداد فارسی به انگلیسی هنگام drop
        input.addEventListener('drop', function(e) {
            setTimeout(() => {
                this.value = convertPersianToEnglish(this.value);
                limitOTPCode(this);
            }, 0);
        });
    });
}); 