from django import forms
from django.forms import ModelForm, Textarea, CheckboxInput
from .models import Ad
from django.utils.translation import ugettext_lazy as _

# class FavForm(forms.Form):
#     # test_input = forms.CharField(widget=forms.Textarea)
#     add_favourite = forms.BooleanField(required=False)
#     # request_borrow = forms.BooleanField(required=False)


class FavForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ('add_fav',)
        # widgets={'add_fav': CheckboxInput()}
        labels = {'add_fav': _('Add to Favourites'),}

class RequestForm(forms.Form):
    request = forms.BooleanField(required=False)
