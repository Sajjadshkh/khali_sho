from django.shortcuts import render
from django.views.generic import ListView
from .models import Aboutus

class AboutUsView(ListView):
    template_name = 'us/aboutus.html'
    model = Aboutus
    context_object_name = 'aboutus'

class PodcastsView(ListView):
    template_name = 'us/podcasts.html'
    model = Aboutus
    context_object_name = 'aboutus'


