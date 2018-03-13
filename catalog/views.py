from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Ad
from . forms import AdDetailForm

def index(request):
    return render(request,'index.html',context={})

class AdListView(generic.ListView):
    # model = Ad
    # Get only active ads
    queryset = Ad.objects.filter(loan_status='a')

class AdUpdateView(generic.UpdateView):
    model = Ad
    fields = '__all__'

class UserAdsListView(LoginRequiredMixin,generic.ListView):
    template_name ='catalog/ad_list_user.html'

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

    # if a GET (or any other method), create blank form
    else:
        form = AdDetailForm()

    context = {'form':form, 'ad':cur_ad}
    return render(request, 'catalog/ad_detail.html', context)
