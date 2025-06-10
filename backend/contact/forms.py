from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.ChoiceField(choices=[
        ('', 'Please choose a category'),
        ('delivery', 'Delivery'),
        ('support', 'Support'),
        ('profile', 'Profile'),
        ('careers', 'Careers'),
        ('another', 'Another category'),
    ])
    message = forms.CharField(widget=forms.Textarea)