from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path('my_ads/', views.UserAdsListView.as_view(), name='my_ads'),
    path('ads/', views.AdListView.as_view(), name='ads'),
    # path('ad/<uuid:pk>', views.AdDetailView.as_view(), name='ad_detail'),
    path('ad/<uuid:ad_pk>', views.get_ad_detail, name='ad_detail'),
    path('ad/<uuid:ad_pk>/fav', views.update_fav, name='update_fav'),
    path('ad/<uuid:ad_pk>/request', views.add_request, name='request_ad'),
    path('ad/<uuid:ad_pk>/cancel-remove', views.cancel_request, name='cancel_request'),
    path('ad/<uuid:ad_pk>/update', views.AdUpdateView.as_view(), name='ad_update'),
    path('ad/<uuid:ad_pk>/delete', views.AdDeleteView.as_view(), name='ad_delete'),
    path('ad/create', views.AdCreate.as_view(), name='ad_create'),
]
