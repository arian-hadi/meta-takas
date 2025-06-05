from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "homepage/homepage.html"

class AboutUsView(TemplateView):
    template_name = "homepage/aboutus.html"