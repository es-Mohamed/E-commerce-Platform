from django import forms

from django.utils.translation import gettext_lazy as _lazy 

from .models import Item

INPUT_class = 'w-full py-4 px-6 rounded-xl border-2 border-solid'

class NewItemform(forms.ModelForm):
    class Meta:
        model= Item
        fields = ("category","name","description","price","image")
        widgets = {
                'category': forms.Select(attrs={
                    'class': INPUT_class
                }),

                'name': forms.TextInput(attrs={
                    'class': INPUT_class
                }),

                'description': forms.Textarea(attrs={
                    'class': INPUT_class
                }),

                'price': forms.TextInput(attrs={
                    'class': INPUT_class
                }),

                'image': forms.FileInput(attrs={
                    'class': INPUT_class
                })
        }

        labels = {
            'category': _lazy('category'),
            'name': _lazy('name'),
            'description': _lazy('Description'),
            'price': _lazy('Price'),
            'image': _lazy('Image'),
        }

class EditItemform(forms.ModelForm):
    class Meta:
        model= Item
        fields = ("name","description","price","image", "is_sold")
        widgets = {

                'name': forms.TextInput(attrs={
                    'class': INPUT_class
                }),

                'description': forms.Textarea(attrs={
                    'class': INPUT_class
                }),

                'price': forms.TextInput(attrs={
                    'class': INPUT_class
                }),

                'image': forms.FileInput(attrs={
                    'class': INPUT_class
                }),

                'is_sold': forms.CheckboxInput(attrs={
                    'class': "py-4 px-6 rounded-xl border-2 border-solid"
                }),

        }

        labels = {
            'name': _lazy('name'),
            'description': _lazy('Description'),
            'price': _lazy('Price'),
            'image': _lazy('Image'),
            'is_sold': _lazy('Is Sold'), 
        }