from django.urls import path
from .views import *

app_name = 'info'

urlpatterns = [
    path("profile_information", ProfileView.as_view(), name = 'profile_information'),

]