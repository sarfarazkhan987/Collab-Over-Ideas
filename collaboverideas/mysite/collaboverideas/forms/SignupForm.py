from django import forms


class SignupForm(forms.Form):
    firstname = forms.CharField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField()
