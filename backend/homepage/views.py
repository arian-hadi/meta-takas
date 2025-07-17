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


#Exchange Rules
class HowItWorksView(TemplateView):
    template_name = "homepage/howitworks.html"

class CreateListingView(TemplateView):
    template_name = "homepage/create_listing.html"


class ExchangeRulesView(TemplateView):
    template_name = "homepage/exchange_rules.html"


class ValuationView(TemplateView):
    template_name = "homepage/valuation.html"


#SUPPORT
class HelpCenterView(TemplateView):
    template_name = "homepage/help_center.html"

class FAQView(TemplateView):
    template_name = "homepage/faq.html"


#LEGAL
class TermsOfUseView(TemplateView):
    template_name = "homepage/terms_of_use.html"

class PrivacyPolicyView(TemplateView):
    template_name = "homepage/privacy_policy.html"

class CookiePolicyView(TemplateView):  
    template_name = "homepage/cookie_policy.html"

class CommunityGuidelinesView(TemplateView):
    template_name = "homepage/community_guidelines.html"

#ABOUT

class OurMissionView(TemplateView):
    template_name = "homepage/our_mission.html"