from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path('ads/', views.AdListView.as_view(), name='ads'),
    path('ad/<uuid:pk>', views.AdDetailView.as_view(), name='ad-detail'),
    path('ad/update/<uuid:ad_pk>', views.get_test_form, name='ad_update'),
    path('ad/create', views.AdCreate.as_view(), name='ad_create'),
]
