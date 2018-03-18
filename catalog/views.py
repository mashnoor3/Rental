from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Ad
from . forms import FavForm

def index(request):
    return render(request,'index.html',context={})

class AdListView(generic.ListView):
    model = Ad
    # Get only active ads
    def get_queryset(self):
        return Ad.objects.filter(loan_status='a')
    # def get_queryset(self):
    #     return Ad.objects.filter(favourites=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super(AdListView, self).get_context_data(**kwargs)
        fav_list = Ad.objects.filter(favourites=self.request.user.profile).values_list('title', flat=True)
        context['fav_list'] = fav_list
        return context

class UserAdsListView(LoginRequiredMixin,generic.ListView):
    template_name ='catalog/ad_list_user.html'
    context_object_name = 'my_ads'

    def get_queryset(self):
        return Ad.objects.filter(renter=self.request.user.profile)

class AdCreate(LoginRequiredMixin, generic.CreateView):
    model = Ad
    fields = ['title', 'description', 'location', 'category', 'loan_duration', 'price']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.renter = self.request.user.profile
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

    show_fav_form = True
    if cur_ad.renter == request.user.profile:
        show_fav_form = False

    if request.method == 'POST':

        fav_form= FavForm(request.POST)
        print(fav_form)
        if fav_form.is_valid():
            pass
    else:
        fav_form= FavForm(instance=cur_ad)

    context = {'fav_form':fav_form, 'ad':cur_ad, 'show_fav_form':show_fav_form}
    return render(request, 'catalog/ad_detail.html', context)

def update_fav(request, ad_pk):
    cur_ad = get_object_or_404(Ad, id=ad_pk)
    if cur_ad:
        fav_list = Ad.objects.filter(favourites=request.user.profile)
        if cur_ad in fav_list:
            cur_ad.favourites.remove(request.user.profile)
        else:
            cur_ad.favourites.add(request.user.profile)

    return HttpResponseRedirect(reverse("ads"))
