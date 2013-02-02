from django import forms

class LastFMSourceForm(forms.Form):
    api_key = forms.CharField()
    api_secret = forms.CharField()
    username = forms.CharField()