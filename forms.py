from django import forms

class RegistrationForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    text = forms.CharField(widget=forms.Textarea)
    
    