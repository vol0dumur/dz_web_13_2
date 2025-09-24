from django import forms
from .models import Tag, Quote, Author


class TagForm(forms.ModelForm):
    name = forms.CharField(
        min_length=3,
        max_length=25,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(forms.ModelForm):
    quote_text = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3})
    )

    class Meta:
        model = Quote
        fields = ['quote_text', 'author']


class AuthorForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    born = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    location = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4})
    )

    class Meta:
        model = Author
        fields = ['name', 'born', 'location', 'description']