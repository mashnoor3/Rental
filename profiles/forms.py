from django.contrib.auth.models import User
from django import forms

from profiles.models import Profile



class ProfileForm(forms.ModelForm):
    class Meta:
        BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
        model = Profile
        fields = ('first_name','last_name', 'bio', 'location', 'birth_date')
        # birth_date = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
