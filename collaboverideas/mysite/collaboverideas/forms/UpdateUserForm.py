from django import forms


class UpdateUserForm(forms.Form):
    firstname = forms.CharField()
    lastname = forms.CharField(required=False)
    email = forms.EmailField()
    dob = forms.DateField(widget=forms.DateInput(), required=False)
    country = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput())
