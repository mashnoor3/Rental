from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Ad
from . forms import FavForm

def index(request):
    return render(request,'index.html',context={})

class AdListView(generic.ListView):
    # model = Ad
    # Get only active ads
    queryset = Ad.objects.filter(loan_status='a')

class UserAdsListView(LoginRequiredMixin,generic.ListView):
    template_name ='catalog/ad_list_user.html'
    context_object_name = 'my_ads'

    def get_queryset(self):
        return Ad.objects.filter(renter=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(UserAdsListView, self).get_context_data(**kwargs)
        context['cur_user'] = self.request.user
        return context

class AdCreate(LoginRequiredMixin, generic.CreateView):
    model = Ad
    fields = ['title', 'description', 'location', 'category', 'loan_duration', 'price']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.renter = self.request.user
        self.object.save()
        return super().form_valid(form)

class AdUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ad
    fields = ['title', 'description', 'location', 'category', 'loan_duration', 'price']
    # To override default update page, uncomment line below
    template_name = "catalog/ad_update.html"

    # Override by default it is set to pk. Change this to ad_pk
    pk_url_kwarg = "ad_pk"

class AdDeleteView(DeleteView):
    model = Ad
    pk_url_kwarg = "ad_pk"
    success_url = reverse_lazy('my_ads')

def get_ad_detail(request, ad_pk):
    cur_ad = Ad.objects.filter(id=ad_pk).get()
    fav_form= FavForm(request.POST or None, instance=cur_ad)

    if request.method == 'POST' and fav_form.is_valid():
        print(fav_form['add_fav'].value())
        # If favourites box is checked, add to user to the Ads favourites attribute
        if fav_form['add_fav'].value() == True:
            cur_ad.favourites.add(request.user.profile)
        else:
            cur_ad.favourites.remove(request.user.profile)

    context = {'fav_form':fav_form, 'ad':cur_ad}
    return render(request, 'catalog/ad_detail.html', context)

def reqeust_borrow(request, ad_pk):
    return render(request, 'catalog/ad_detail.html', {})
