#!/usr/bin/env python
"""
فایل تست برای سیستم خرید و پرداخت
"""

import os
import sys
import django

# تنظیم Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'khali_sho.settings')
django.setup()

from us.models import Plan, Cart, CartItem, Order, OrderItem
from django.contrib.sessions.models import Session
from django.utils import timezone

def test_plan_creation():
    """تست ایجاد پلن‌ها"""
    print("=== تست ایجاد پلن‌ها ===")
    
    # ایجاد پلن تلفنی
    phone_plan = Plan.objects.create(
        name='پلن تست تلفنی',
        plan_type='phone',
        duration=30,
        extra_time=5,
        price=150000,
        is_active=True
    )
    print(f"پلن تلفنی ایجاد شد: {phone_plan}")
    
    # ایجاد پلن حضوری
    inperson_plan = Plan.objects.create(
        name='پلن تست حضوری',
        plan_type='inperson',
        duration=60,
        extra_time=10,
        price=280000,
        is_active=True
    )
    print(f"پلن حضوری ایجاد شد: {inperson_plan}")
    
    return phone_plan, inperson_plan

def test_cart_operations():
    """تست عملیات سبد خرید"""
    print("\n=== تست عملیات سبد خرید ===")
    
    # ایجاد session
    session = Session.objects.create(
        session_key='test_session_key',
        expire_date=timezone.now() + timezone.timedelta(days=1)
    )
    
    # ایجاد سبد خرید
    cart = Cart.objects.create(session_key=session.session_key)
    print(f"سبد خرید ایجاد شد: {cart}")
    
    # ایجاد پلن‌ها
    phone_plan, inperson_plan = test_plan_creation()
    
    # اضافه کردن آیتم به سبد خرید
    cart_item1 = CartItem.objects.create(
        cart=cart,
        plan=phone_plan,
        quantity=2
    )
    print(f"آیتم اول اضافه شد: {cart_item1}")
    
    cart_item2 = CartItem.objects.create(
        cart=cart,
        plan=inperson_plan,
        quantity=1
    )
    print(f"آیتم دوم اضافه شد: {cart_item2}")
    
    # محاسبه قیمت کل
    total_price = cart.get_total_price()
    print(f"قیمت کل سبد خرید: {total_price:,} تومان")
    
    return cart, total_price

def test_order_creation():
    """تست ایجاد سفارش"""
    print("\n=== تست ایجاد سفارش ===")
    
    cart, total_price = test_cart_operations()
    
    # ایجاد سفارش
    order = Order.objects.create(
        phone='09123456789',
        total_amount=total_price,
        status='pending'
    )
    print(f"سفارش ایجاد شد: {order}")
    print(f"شماره سفارش: {order.order_number}")
    
    # انتقال آیتم‌ها از سبد خرید به سفارش
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            plan=cart_item.plan,
            quantity=cart_item.quantity,
            price=cart_item.plan.price,
            total_price=cart_item.get_total_price()
        )
        print(f"آیتم سفارش ایجاد شد: {cart_item.plan.name}")
    
    # نمایش جزئیات سفارش
    print(f"\nجزئیات سفارش {order.order_number}:")
    for item in order.items.all():
        print(f"- {item.plan.name}: {item.quantity} عدد × {item.price:,} تومان = {item.total_price:,} تومان")
    print(f"مجموع کل: {order.total_amount:,} تومان")
    
    return order

def test_payment_simulation():
    """تست شبیه‌سازی پرداخت"""
    print("\n=== تست شبیه‌سازی پرداخت ===")
    
    order = test_order_creation()
    
    # شبیه‌سازی پرداخت موفق
    order.status = 'paid'
    order.payment_id = f'PAY_{order.order_number}_12345'
    order.save()
    
    print(f"پرداخت موفق برای سفارش {order.order_number}")
    print(f"شناسه پرداخت: {order.payment_id}")
    print(f"وضعیت: {order.get_status_display()}")

def cleanup_test_data():
    """پاک کردن داده‌های تست"""
    print("\n=== پاک کردن داده‌های تست ===")
    
    # پاک کردن سفارشات
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    
    # پاک کردن سبد خرید
    CartItem.objects.all().delete()
    Cart.objects.all().delete()
    
    # پاک کردن پلن‌ها
    Plan.objects.filter(name__contains='تست').delete()
    
    # پاک کردن session
    Session.objects.filter(session_key='test_session_key').delete()
    
    print("داده‌های تست پاک شدند")

def main():
    """تابع اصلی تست"""
    print("شروع تست سیستم خرید و پرداخت")
    print("=" * 50)
    
    try:
        # اجرای تست‌ها
        test_payment_simulation()
        
        print("\n" + "=" * 50)
        print("تمام تست‌ها با موفقیت انجام شدند!")
        
    except Exception as e:
        print(f"\nخطا در اجرای تست: {e}")
        
    finally:
        # پاک کردن داده‌های تست
        cleanup_test_data()

if __name__ == '__main__':
    main() 