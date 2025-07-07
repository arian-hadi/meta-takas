from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        from .utils.city_data import PROVINCE_MAP
        super().__init__(*args, **kwargs)
        selected_city = (
            self.data.get('city') or
            self.initial.get('city') or
            getattr(self.instance, 'city', None)
        )

        if selected_city in PROVINCE_MAP:
            self.fields["province"].widget = forms.Select(
                choices=[(p, p) for p in PROVINCE_MAP[selected_city]]
            )
        else:
            self.fields["province"].widget = forms.Select(choices=[])
