from modeltranslation.translator import translator, TranslationOptions

from .models import Category, Item

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

class ItemTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'price')
    

translator.register(Category, CategoryTranslationOptions)
translator.register(Item, ItemTranslationOptions)