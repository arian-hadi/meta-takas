from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
import logging

from .forms import CustomUserCreationForm, OTPVerificationForm, EmailAuthenticationForm, CustomPasswordResetForm
from .models import CustomUser, OneTimePassword
from .utils.email_utils import send_code_to_user

logger = logging.getLogger(__name__)


class RegisterUserView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        print(f"Sending email to: {user.email}")

        if not user.email or "@" not in user.email:
            return self.form_invalid(form)

        self.request.session["user_email"] = user.email

        send_code_to_user(user.email)
        messages.success(self.request, "OTP sent! Please check your email.")

        return redirect('verify_email')



class VerifyUserEmail(View):
    def get(self, request):
        user_email = request.session.get("user_email")
        if not user_email:
            messages.error(request, "Session expired. Please request a new OTP.")
            return redirect("signup")

        form = OTPVerificationForm()
        return render(request, "accounts/verify_email.html", {"form": form})

    def post(self, request):
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data["otp_code"]
            user_email = request.session.get("user_email")

            if not user_email:
                messages.error(request, "Session expired. Please request a new OTP.")
                return redirect("signup")

            try:
                user = CustomUser.objects.get(email=user_email)
                otp_entry = OneTimePassword.objects.filter(user=user, code=otp_code).first()

                if not otp_entry or otp_entry.is_expired():
                    messages.error(request, "Invalid or expired OTP. Please try again.")
                    return render(request, "accounts/verify_email.html", {"form": form})

                user.is_verified = True
                user.is_active = True
                user.save(update_fields=["is_active", "is_verified"])
                otp_entry.delete()

                request.session.pop("user_email", None)

                messages.success(request, "Email verified successfully! You can now log in.")
                return redirect("login")

            except CustomUser.DoesNotExist:
                messages.error(request, "User does not exist.")

        return render(request, "accounts/verify_email.html", {"form": form})


class ResendOTPView(View):
    def get(self, request):
        email = request.session.get("user_email")
        if not email:
            messages.error(request, "Session expired. Please sign up again.")
            return redirect("signup")

        try:
            user = CustomUser.objects.get(email=email)
            send_code_to_user(user.email)
            messages.success(request, "A new OTP has been sent to your email.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")

        return redirect("verify_email")


class EmailLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = form.get_user()
        logger.info(f"Attempting login for user: {user.email}")

        if not user.is_verified:
            logger.warning(f"User {user.email} is not verified")
            messages.error(self.request, "Please verify your email before logging in.")
            return self.form_invalid(form)

        if not user.is_active:
            logger.warning(f"User {user.email} is not active")
            messages.error(self.request, "Your account is not active.")
            return self.form_invalid(form)

        login(self.request, user)
        logger.info(f"User {user.email} logged in successfully.")

        # ✅ Simplified redirection — just go to homepage
        return redirect('home')

    def form_invalid(self, form):
        logger.warning("Login failed.")
        messages.error(self.request, "Invalid email or password.")
        return super().form_invalid(form)


class ContinueVerificationView(View):
    def get(self, request):
        return render(request, "accounts/continue_verification.html")

    def post(self, request):
        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(email=email)
            if user.is_verified:
                messages.info(request, "This account is already verified.")
                return redirect("login")

            request.session["user_email"] = email
            messages.success(request, "Session restored. Please verify your OTP.")
            return redirect("verify_email")
        except CustomUser.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect("continue_verification")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('homepage')


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    email_template_name = 'registration/password_reset_email.txt'
    html_email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
