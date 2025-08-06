from modeltranslation.translator import translator, TranslationOptions
from .models import Category

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)  # Translate the 'name' field

translator.register(Category, CategoryTranslationOptions)
