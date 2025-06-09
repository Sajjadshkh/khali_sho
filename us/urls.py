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
    path("podcast/create/", views.PodcastCreateView.as_view(), name='podcast_create'),
    # path('pushpodcast/', views.OTPView.as_view(), name='pushpodcast'),
    path('otp/', views.OTPView.as_view(), name='otp'),
    path('checkotp/', views.CheckOTPView.as_view(), name='checkotp'),
    # path('workwithus/', views.WorkWithUsView.as_view(), name='workwithus'),

]
