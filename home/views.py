from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from us.models import Adviser
from accounts.models import Testimonial

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advisers'] = Adviser.objects.filter(is_approved=True, is_featured=True).order_by('-id')[:3]
        context['testimonials'] = Testimonial.objects.filter(is_active=True).order_by('-created_at')
        return context

class TopAdvisersView(ListView):
    model = Adviser
    template_name = 'home/home.html'
    context_object_name = 'advisers'

    def get_queryset(self):
        return Adviser.objects.filter(is_approved=True, is_featured=True).order_by('-id')[:3]

def custom_404(request, exception):
    return render(request, '404/404.html', status=404)

