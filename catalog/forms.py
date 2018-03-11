from django import forms

class TestForm(forms.Form):
    test_input = forms.CharField(widget=forms.Textarea)
    check_me = forms.BooleanField(required=False)
