from django import forms

class RegistrationForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    file = forms.FileField(help_text=u"Upload a file with the following format on each line: metadata$$$sentencehere")