from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from accounts.models import CustomUser
from accounts.forms import ProfileForm
from django.views.generic import TemplateView

# Create your views here.
class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = "info/profile_information.html"
    success_url = reverse_lazy('profile_information')

    def get_object(self, queryset=None):
        return self.request.user

class ManageAddressView(TemplateView):
    template_name = "info/manage_address.html"


class ChangePasswordView(TemplateView):
    template_name = "info/change_password.html"


class WishListView(TemplateView):
    template_name = "info/wishlist.html"


class ManageAccountView(TemplateView):
    template_name = "info/manage_account.html"