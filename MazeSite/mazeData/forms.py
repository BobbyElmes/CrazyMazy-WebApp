from django import forms

class Register(forms.Form):
    username = forms.CharField(label='username', max_length=35)
    password = forms.CharField(label='password', max_length=35)