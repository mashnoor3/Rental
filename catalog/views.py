from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Ad #Tool

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

class AdDetailView(generic.DetailView):
    model = Ad


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







# class ToolListView(generic.ListView):
#     model = Tool
#
#     def get_context_data(self, **kwargs):
#         # Need to call the base implementation first to get the context
#         context = super(ToolListView, self).get_context_data(**kwargs)
#         context['some_data'] = 'lala'
#         return context
#
# class ToolDetailView(generic.DetailView):
#     model = Tool
