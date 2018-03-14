from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from django.contrib.auth.forms import UserCreationForm

from .forms import UserForm, ProfileForm
from .models import Profile
from catalog.models import Ad

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

class FavouriteListView(generic.ListView, LoginRequiredMixin):
    model = Ad
    context_object_name = 'my_favourites_list'
    template_name ='my-favourites.html'

    # Override the refault queryset of Listview to return Ads that have favourites set to current user
    def get_queryset(self):
        return Ad.objects.filter(favourites=self.request.user.profile)
