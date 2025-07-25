from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path('', views.TopAdvisersView.as_view(), name='top_advisers'),
]
