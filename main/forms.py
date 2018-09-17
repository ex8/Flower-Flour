from django import forms
from main.models import Contact, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'body')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': "Name",
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone'
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Message'
            })
        }
