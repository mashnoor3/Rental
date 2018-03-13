from django import forms

class AdDetailForm(forms.Form):
    # test_input = forms.CharField(widget=forms.Textarea)
    add_favourite = forms.BooleanField(required=False)
