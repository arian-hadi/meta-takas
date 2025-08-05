from django import forms
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.ChoiceField(choices=[
        ('', _("Please select a category")),
        ('delivery', _("Delivery")),
        ('support', _("Support")),
        ('profile', _("Profile")),
        ('careers', _("Careers")),
        ('another', _("Other category")),
    ])
    message = forms.CharField(widget=forms.Textarea)