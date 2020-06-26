from django import forms


class FileUploadForm(forms.Form):
    fileName=forms.CharField()
    fileType=forms.CharField()