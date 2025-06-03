from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
import logging
from django.core.exceptions import ValidationError
from PIL import Image

logger = logging.getLogger(__name__)
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, label="First Name")
    last_name = forms.CharField(max_length=30, required=False, label="Last Name")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser  # <-- important correction here!
        fields = ['email', 'username', 'first_name', 'last_name']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
from django import forms
from .models import CustomUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar', 'first_name', 'last_name']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={
                'accept': 'image/*',
                'class': 'w-full border px-4 py-2 lg:w-1/2'
            }),
            'first_name': forms.TextInput(attrs={'class': 'w-full border px-4 py-2 lg:w-1/2'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full border px-4 py-2 lg:w-1/2'}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            try:
                img = Image.open(avatar)
                width, height = img.size

                if width != height:
                    raise forms.ValidationError("Avatar must have a 1:1 aspect ratio (square).")

                max_resolution = 500
                if width > max_resolution or height > max_resolution:
                    raise forms.ValidationError(f"Maximum allowed resolution is {max_resolution}x{max_resolution} pixels.")

            except Exception:
                raise forms.ValidationError("Invalid image file.")

        return avatar

    
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(  # Keep this as username but change the field name in template
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg text-sm',
            'placeholder': 'Enter your email'
        })
    )
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'mt-1 block w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg text-sm',
        'placeholder': 'Enter your password'
    }))

    def clean(self):
        username = self.cleaned_data.get('username')  # This is actually the email
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password)
            if self.user_cache is None:
                raise ValidationError(
                    'Invalid email or password.',
                    code='invalid_login'
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class CustomPasswordResetForm(PasswordResetForm):
    def save(self, *args, **kwargs):
        user = self.get_users(self.cleaned_data["email"])
        for u in user:
            logger.info(f"User ID: {u.id}, Email: {u.email}")
        super().save(*args, **kwargs)


class OTPVerificationForm(forms.Form):
    otp_code = forms.CharField(
        label = "Enter OTP",
        max_length = 6,
        min_length = 6,
        widget=forms.TextInput(attrs={'placeholder': 'Enter 6-digit OTP'})
    )