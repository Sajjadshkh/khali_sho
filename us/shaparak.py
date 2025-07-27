import requests
import hashlib
import json
from django.conf import settings
from django.urls import reverse

class ShaparakPayment:
    """
    کلاس مدیریت پرداخت از طریق درگاه شاپرک
    """
    
    def __init__(self):
        # تنظیمات درگاه شاپرک - این مقادیر باید در settings.py تعریف شوند
        self.terminal_id = getattr(settings, 'SHAPARAK_TERMINAL_ID', '')
        self.merchant_id = getattr(settings, 'SHAPARAK_MERCHANT_ID', '')
        self.callback_url = getattr(settings, 'SHAPARAK_CALLBACK_URL', '')
        self.api_url = getattr(settings, 'SHAPARAK_API_URL', 'https://api.shaparak.ir')
        
    def create_payment_request(self, order, amount, description):
        """
        ایجاد درخواست پرداخت
        """
        try:
            # تولید شناسه یکتا برای تراکنش
            transaction_id = f"TXN_{order.order_number}_{order.id}"
            
            # پارامترهای درخواست
            payment_data = {
                'terminal_id': self.terminal_id,
                'merchant_id': self.merchant_id,
                'amount': int(amount),  # مبلغ به ریال
                'order_id': order.order_number,
                'transaction_id': transaction_id,
                'callback_url': f"{self.callback_url}{reverse('us:payment_callback', args=[order.id])}",
                'description': description,
                'currency': 'IRR',  # ریال ایران
                'language': 'fa',   # فارسی
            }
            
            # ایجاد امضای دیجیتال
            signature = self._create_signature(payment_data)
            payment_data['signature'] = signature
            
            # ارسال درخواست به درگاه
            response = requests.post(
                f"{self.api_url}/payment/request",
                json=payment_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    return {
                        'success': True,
                        'payment_url': result.get('payment_url'),
                        'transaction_id': transaction_id,
                        'reference_id': result.get('reference_id')
                    }
                else:
                    return {
                        'success': False,
                        'error': result.get('message', 'خطا در ایجاد درخواست پرداخت')
                    }
            else:
                return {
                    'success': False,
                    'error': f'خطا در ارتباط با درگاه: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'خطا در پردازش درخواست: {str(e)}'
            }
    
    def verify_payment(self, reference_id, transaction_id):
        """
        تایید پرداخت
        """
        try:
            verify_data = {
                'terminal_id': self.terminal_id,
                'merchant_id': self.merchant_id,
                'reference_id': reference_id,
                'transaction_id': transaction_id,
            }
            
            # ایجاد امضای دیجیتال
            signature = self._create_signature(verify_data)
            verify_data['signature'] = signature
            
            # ارسال درخواست تایید
            response = requests.post(
                f"{self.api_url}/payment/verify",
                json=verify_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    return {
                        'success': True,
                        'amount': result.get('amount'),
                        'transaction_id': result.get('transaction_id'),
                        'reference_id': result.get('reference_id')
                    }
                else:
                    return {
                        'success': False,
                        'error': result.get('message', 'خطا در تایید پرداخت')
                    }
            else:
                return {
                    'success': False,
                    'error': f'خطا در ارتباط با درگاه: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'خطا در پردازش تایید: {str(e)}'
            }
    
    def _create_signature(self, data):
        """
        ایجاد امضای دیجیتال
        """
        # ترتیب فیلدها برای ایجاد امضا
        signature_fields = [
            'terminal_id',
            'merchant_id', 
            'amount',
            'order_id',
            'transaction_id',
            'callback_url'
        ]
        
        # ایجاد رشته امضا
        signature_string = ""
        for field in signature_fields:
            if field in data:
                signature_string += str(data[field]) + "#"
        
        # اضافه کردن کلید خصوصی
        private_key = getattr(settings, 'SHAPARAK_PRIVATE_KEY', '')
        signature_string += private_key
        
        # ایجاد هش SHA256
        signature = hashlib.sha256(signature_string.encode('utf-8')).hexdigest()
        
        return signature

# نمونه استفاده
def process_shaparak_payment(order):
    """
    پردازش پرداخت از طریق درگاه شاپرک
    """
    shaparak = ShaparakPayment()
    
    # ایجاد درخواست پرداخت
    payment_result = shaparak.create_payment_request(
        order=order,
        amount=order.total_amount * 10,  # تبدیل تومان به ریال
        description=f"پرداخت سفارش {order.order_number}"
    )
    
    return payment_result 