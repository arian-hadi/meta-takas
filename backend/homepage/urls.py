from django.urls import path
from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name = 'homepage'),
    path("aboutus/", AboutUsView.as_view(), name = 'aboutus'),

]