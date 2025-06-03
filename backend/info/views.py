from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class ProfileView(TemplateView):
    template_name = "info/profile_information.html"

class ManageAddressView(TemplateView):
    template_name = "info/manage_address.html"


class ChangePasswordView(TemplateView):
    template_name = "info/change_password.html"


class WishListView(TemplateView):
    template_name = "info/wishlist.html"


class ManageAccountView(TemplateView):
    template_name = "info/manage_account.html"