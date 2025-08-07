from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product, ProductDetailRow

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


@register(ProductDetailRow)
class ProductDetailRowTranslationOptions(TranslationOptions):
    fields = ('label', 'value')