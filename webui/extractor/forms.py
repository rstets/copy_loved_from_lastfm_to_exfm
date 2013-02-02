from django import forms


class LastFMSourceForm(forms.Form):
    SOURCE_TITLE = 'LastFM source extractor'

    username = forms.CharField()
    limit = forms.CharField()