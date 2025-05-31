from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView

from .views import *
from .views import (
    RegisterUserView, VerifyUserEmail, EmailLoginView, CustomLogoutView,
    CustomPasswordResetView, CustomPasswordResetConfirmView
)


urlpatterns = [

    path('signup/', RegisterUserView.as_view(), name='signup'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify_email'),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('continue-verification/', ContinueVerificationView.as_view(), name='continue_verification'),

    # Password Reset URLs
    path('password-reset/', CustomPasswordResetView.as_view(template_name="registration/password_reset_form.html"), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),

]