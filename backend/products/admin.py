from django.contrib import admin

from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVideo

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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'category', 'listing_type', 'price', 'city', 'created_at']
    search_fields = ['name', 'description', 'city']
    list_filter = ['category', 'city', 'listing_type']
    inlines = [ProductImageInline, ProductVideoInline]
    filter_horizontal = ('exchange_for',)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser


