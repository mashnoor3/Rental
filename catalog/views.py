from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Ad

def index(request):
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={},
    )

class AdListView(generic.ListView):
    # To get all Ads. model = Ad is really just shorthand for saying queryset = Ad.objects.all()
    # model = Ad
    # To get only active ads
    queryset = Ad.objects.filter(loan_status='a')

class AdUpdateView(generic.UpdateView):
    model = Ad
    fields = '__all__'


class AdDetailView(generic.DetailView):
    model = Ad

    def get_context_data(self, **kwargs):
        context = super(AdDetailView, self).get_context_data(**kwargs)
        # context['fav_user'] = self.request.user.profile
        context['fav_user'] = Ad.objects.filter(favourites=self.request.user.profile)
        return context

class UserAdsListView(LoginRequiredMixin,generic.ListView):
    model = Ad
    template_name ='catalog/ad_list_user.html'

# -----------------------CRUD Views---------------------------------------------
class AdCreate(LoginRequiredMixin, generic.CreateView):
    # fields = ('title', 'description', 'loan_duration', 'price')
    model = Ad
    fields = ['title', 'description', 'location', 'category', 'loan_duration', 'price']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.renter = self.request.user
        self.object.save()
        return super().form_valid(form)

from . forms import AdDetailForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def get_ad_detail_form(request, ad_pk):
    cur_ad = Ad.objects.filter(id=ad_pk).get()
    if request.method == 'POST':
        form = AdDetailForm(request.POST)
        if form.is_valid():

            if form['add_favourite'].value() == True:
                cur_ad.favourites.add(request.user.profile)
            else:
                cur_ad.favourites.remove(request.user.profile)
            print(cur_ad.favourites.all())
            return HttpResponseRedirect(reverse("ads"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AdDetailForm()
    print (cur_ad.title)
    print (cur_ad.price)
    context = {'form':form, 'title':cur_ad.title, 'price':cur_ad.price}
    return render(request, 'catalog/ad_update.html', context)
