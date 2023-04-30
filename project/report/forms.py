from django import forms


class MyForm(forms.Form):
    first = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg mt-2 mb-4  required:required', }))
    second = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg mt-2 mb-4  required:required', }))
    third = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg mt-2 mb-4  required:required', }))
