from django.shortcuts import render
from django.views.generic import ListView, TemplateView

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home/home.html'

def custom_404(request, exception):
    return render(request, '404/404.html', status=404)