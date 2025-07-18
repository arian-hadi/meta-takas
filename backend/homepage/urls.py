from django.urls import path
from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name = 'homepage'),
    path("aboutus/", AboutUsView.as_view(), name = 'aboutus'),
    path("howitworks/", HowItWorksView.as_view(), name = 'howitworks'),
    path("create_listing/", CreateListingView.as_view(), name = 'create_listing'),
    path("exchange_rules/", ExchangeRulesView.as_view(), name = 'exchange_rules'),
    path("valuation/", ValuationView.as_view(), name = 'valuation'),
    path("help_center/", HelpCenterView.as_view(), name = 'help_center'),
    path("terms_of_use/", TermsOfUseView.as_view(), name = 'terms_of_use'),
    path("privacy_policy/", PrivacyPolicyView.as_view(), name = 'privacy_policy'),
    path("cookie_policy/", CookiePolicyView.as_view(), name = 'cookie_policy'),
    path("community_guidelines/", CommunityGuidelinesView.as_view(), name = 'community_guidelines'),
    path("our_mission/", OurMissionView.as_view(), name = 'our_mission'),

]