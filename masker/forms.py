from django import forms

class MaskerForm(forms.Form):
    text = forms.CharField(required=False)
