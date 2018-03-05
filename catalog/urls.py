from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    # path('tools/', views.ToolListView.as_view(), name='tools'),
    # path('tool/<int:pk>', views.ToolDetailView.as_view(), name='tool-detail'),
    path('ads/', views.AdListView.as_view(), name='ads'),
    path('ad/<uuid:pk>', views.AdDetailView.as_view(), name='ad-detail'),
    path('ad/create', views.AdCreate.as_view(), name='ad_create'),
]
