from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.mail import send_mail
from .forms import ContactForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.core.mail import EmailMessage
from django.conf import settings


class ContactUsView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']

        full_message = (
            f"New message from contact form:\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Subject: {subject}\n\n"
            f"Message:\n{message}"
        )

        email_message = EmailMessage(
            subject=f"Contact Form: {subject}",
            body=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,  # ✅ This uses your authenticated email
            to=[settings.DEFAULT_FROM_EMAIL],         # ✅ Send to yourself
            reply_to=[email],                         # ✅ Allows you to reply to the sender
        )

        try:
            email_message.send()
            messages.success(self.request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(self.request, "There was an error sending your message.")
            # Optional: log or print the error for debugging
            print(f"Email sending failed: {e}")

        return super().form_valid(form)