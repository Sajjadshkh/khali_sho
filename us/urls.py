from django.urls import path
from . import views

app_name = 'us'
urlpatterns = [
    # path('jobpositions/', views.JobposView.as_view(), name='jobpos'),
    # path('jobdetail/<str:slug>', views.JobDeatailView.as_view(), name='jobdetail'),
    # path("customers/", views.CustomersView.as_view(), name='customers'),
    # path("contactus/", views.ContactUsView.as_view(), name='contactus'),
    path("aboutus/", views.AboutUsView.as_view(), name='aboutus'),
    path("services/", views.ServicesView.as_view(), name='services'),
    path("podcasts/", views.PodcastsView.as_view(), name='podcasts'),
    path("podcast/create/", views.podcast_create, name='podcast_create'),
    path("adviser/create/", views.AdviserCreateView.as_view(), name='adviser_create'),
    path("cafe/create/", views.CafeCreateView.as_view(), name='cafe_create'),
    path('otp/', views.OTPView.as_view(), name='otp'),
    path('checkotp/', views.CheckOTPView.as_view(), name='checkotp'),
    path('aboutus/', views.AllAdvisersView.as_view(), name='aboutus'),
    
    # URL های جدید برای سیستم خرید
    path('add-to-cart/<int:plan_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/<int:order_id>/', views.payment_view, name='payment'),
    path('payment/callback/<int:order_id>/', views.PaymentCallbackView.as_view(), name='payment_callback'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('order/detail/<int:order_id>/', views.order_detail, name='order_detail'),
]
