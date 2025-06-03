from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("profile_information", ProfileView.as_view(), name = 'profile_information'),
    path("manage_address", ManageAddressView.as_view(), name = 'manage_address'),
    path("change_password", ChangePasswordView.as_view(), name = 'change_password'),
    path("wishlist", WishListView.as_view(), name = 'wishlist'),
    path("manage_account", ManageAccountView.as_view(), name = 'manage_account'),
    path('logout/', LogoutView.as_view(next_page='homepage'), name='logout'),

]