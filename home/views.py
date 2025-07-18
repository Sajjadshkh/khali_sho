from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from us.models import adviser

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home/home.html'

class TopAdvisersView(ListView):
    model = adviser
    template_name = 'home/home.html'
    context_object_name = 'advisers'

    def get_queryset(self):
        return adviser.objects.filter(is_featured=True).order_by('-created_at')[:3]

def custom_404(request, exception):
    return render(request, '404/404.html', status=404)

