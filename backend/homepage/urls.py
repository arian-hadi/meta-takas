from django.urls import path
from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name = 'homepage'),
    path("aboutus/", AboutUsView.as_view(), name = 'aboutus'),
    path("howitworks/", HowItWorksView.as_view(), name = 'howitworks'),
    path("create_listing/", CreateListingView.as_view(), name = 'create_listing'),
    path("exchange_rules/", ExchangeRulesView.as_view(), name = 'exchange_rules'),
    path("valuation/", ValuationView.as_view(), name = 'valuation'),

]