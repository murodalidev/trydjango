from django import forms

from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'tags']
        exclude = ['author']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'rows': 2
        })
        self.fields['tags'].widget.attrs.update({
            'class': 'form-control'
        })



class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['recipe', 'title', 'quantity', 'unit']
        exclude = ['recipe']

    def clean_title(self):  # clean_{field_name}
        title = self.data.get('title')
        if not title[0].isupper():
            raise forms.ValidationError("first character must be uppercase")
        return self.data.get('title')

    def __init__(self, *args, **kwargs):
        super(IngredientForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingredient'
        })
        self.fields['quantity'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'example: 300'
        })
        self.fields['unit'].widget.attrs.update({
            'class': 'form-control',
        })


