from django import forms

class RegistrationForm(models.Model):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    text = forms.CharField(widget=forms.Textarea)
    
    