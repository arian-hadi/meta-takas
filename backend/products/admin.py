from django.contrib import admin
import nested_admin
from django import forms
from .models import Category, Product, ProductImage, ProductVideo, ExchangeNote, ExchangeNoteItem
from .utils.city_data import CITY_CHOICES, PROVINCE_MAP
from django import forms

@admin.register(Category)
class CategoryAdmin(nested_admin.NestedModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'slug']


class ProductImageInline(nested_admin.NestedTabularInline):
    model = ProductImage
    extra = 3  # allows adding up to 5 images by default


class ProductVideoInline(nested_admin.NestedTabularInline):
    model = ProductVideo
    extra = 1


class ExchangeNoteItemInline(nested_admin.NestedTabularInline):
    model = ExchangeNoteItem
    extra = 2

class ExchangeNoteInline(nested_admin.NestedTabularInline):
    model = ExchangeNote
    inlines = [ExchangeNoteItemInline]
    extra = 1



class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Always set city choices
        self.fields['city'].widget = forms.Select(choices=CITY_CHOICES)

        # Dynamically set province choices based on selected city
        selected_city = self.data.get('city') or self.initial.get('city')

        if selected_city in PROVINCE_MAP:
            self.fields['province'].widget = forms.Select(
                choices=[(p, p) for p in PROVINCE_MAP[selected_city]]
            )
        else:
            self.fields['province'].widget = forms.Select(choices=[])

@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    form = ProductAdminForm 
    
    class Media:
        js = ('js/admin_city_province.js',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Inject PROVINCE_MAP into the admin page as a JS global
        import json
        from django.utils.safestring import mark_safe
        from .utils.city_data import PROVINCE_MAP

        province_json = json.dumps(PROVINCE_MAP)
        form.base_fields['province'].help_text = mark_safe(
            f'<script>window.PROVINCE_MAP = {province_json};</script>'
        )

        return form


    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'category', 'listing_type', 'price', 'city', 'created_at']
    search_fields = ['name', 'description', 'city']
    list_filter = ['category', 'city', 'listing_type']
    inlines = [ProductImageInline, ProductVideoInline, ExchangeNoteInline]
    filter_horizontal = ('exchange_for',)

        # Field groups
    fieldsets = (
        (None, {
            'fields': (
                'name', 'slug', 'category', 'listing_type', 'price', 'description',
                'image', 'city', 'province', 'neighborhood', 'street', 'postal_code',
                'phone_number', 'whatsapp_number', 'email'
            )
        }),
        ('Exchange Preferences', {
            'fields': (
                'exchange_for', 'exchange_details',
                'min_budget', 'max_budget',
                'will_give_extra_cash',
                'will_receive_extra_cash',
                'cannot_give_extra_cash',
                'accept_half_cash',
                'accept_half_barter',
                'accept_full_barter',
                'accept_full_cash',
            ),
            'classes': ('collapse',),  # collapsible section
        }),
    )


    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser


