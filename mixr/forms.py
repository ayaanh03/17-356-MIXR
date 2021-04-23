from django import forms

class JoinForm(forms.Form):
    code = forms.CharField(max_length = 100)