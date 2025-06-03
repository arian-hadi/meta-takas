from django.urls import path
from .views import *


urlpatterns = [
    path("profile_information", ProfileView.as_view(), name = 'profile_information'),
    path("manage_address", ManageAddressView.as_view(), name = 'manage_address'),
    path("change_password", ChangePasswordView.as_view(), name = 'change_password'),

]