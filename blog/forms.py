from django import forms
from .models import *


class TicketForms(forms.Form):
    SUBJECT_CHOICE = (
        ('Offer', 'Offer'),
        ('Report', 'Report'),
        ('Criticism', 'Criticism'),
    )
    name = forms.CharField(max_length=250, required=True)
    family = forms.CharField(max_length=250, required=True)
    massage = forms.CharField(widget=forms.Textarea, required=True)
    email = forms.EmailField(max_length=250, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICE, required=True)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']


class SearchForm(forms.Form):
    query = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=250, required=True)
    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()


class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('new_password') != cleaned.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned


class UserRegister(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=20, required=True, label='password')
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=20, required=True, label='repeat password')

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class UserEdit(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class AccountEdit(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['bio', 'birth', 'job', 'photos']

