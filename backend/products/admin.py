from django.contrib import admin

from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'slug']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # allows adding up to 5 images by default



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'category', 'price', 'city', 'created_at']
    search_fields = ['name', 'description', 'city']
    list_filter = ['category', 'city']
    inlines = [ProductImageInline]


