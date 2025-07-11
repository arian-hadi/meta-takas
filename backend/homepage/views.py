from django.shortcuts import render
from django.views.generic import TemplateView
from products.models import Product


class HomeView(TemplateView):
    template_name = "homepage/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Product.objects.order_by('-created_at')[:4]
        return context

class AboutUsView(TemplateView):
    template_name = "homepage/aboutus.html"


class TermsView(TemplateView):
    template_name = "homepage/terms.html"

class ConditionsView(TemplateView):
    template_name = "homepage/conditions.html"