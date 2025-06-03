from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from accounts.models import CustomUser
from accounts.forms import ProfileForm
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordChangeView
from .forms import CustomPasswordChangeForm

# Create your views here.
class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = "info/profile_information.html"
    success_url = reverse_lazy('profile_information')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'files': self.request.FILES
        })
        return kwargs

    def form_valid(self, form):
        # Explicit save call ensures all fields get saved correctly
        form.save()
        return super().form_valid(form)


class ManageAddressView(TemplateView):
    template_name = "info/manage_address.html"


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "info/change_password.html"
    success_url = reverse_lazy('profile_information')


class WishListView(TemplateView):
    template_name = "info/wishlist.html"


class ManageAccountView(TemplateView):
    template_name = "info/manage_account.html"


class LogoutView(TemplateView):

    def get(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        logout(request)
        return super().get(request, *args, **kwargs)