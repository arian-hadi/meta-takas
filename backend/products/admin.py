from django.contrib import admin

from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVideo, ExchangeCategoryNote

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'slug']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # allows adding up to 5 images by default


class ProductVideoInline(admin.TabularInline):
    model = ProductVideo
    extra = 1

class ExchangeCategoryNoteInline(admin.TabularInline):
    model = ExchangeCategoryNote
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'category', 'listing_type', 'price', 'city', 'created_at']
    search_fields = ['name', 'description', 'city']
    list_filter = ['category', 'city', 'listing_type']
    inlines = [ProductImageInline, ProductVideoInline, ExchangeCategoryNoteInline]
    filter_horizontal = ('exchange_for',)

        # Field groups
    fieldsets = (
        (None, {
            'fields': (
                'name', 'slug', 'category', 'listing_type', 'price', 'description',
                'image', 'city', 'district', 'neighborhood', 'street', 'postal_code',
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


