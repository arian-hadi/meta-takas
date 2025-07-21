from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.ChoiceField(choices=[
        ('', 'Lütfen bir kategori seçin'),
        ('delivery', 'Teslimat'),
        ('support', ' Destek'),
        ('profile', 'Profil'),
        ('careers', ' Kariyer'),
        ('another', 'Diğer kategori'),
    ])
    message = forms.CharField(widget=forms.Textarea)