from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "image", "body"]

    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            "placeholder": "title...",
            "class": 'form-control',
        })
        self.fields['image'].widget.attrs.update({
            "class": 'form-control',
        })
        self.fields['body'].widget.attrs.update({
            "placeholder": 'body..',
            "class": 'form-control',
            "cols": 21,
            "rows": 3
        })
