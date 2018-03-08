from django.urls import path

from django.contrib.auth import views as auth_views
from . import views as account_views
from profiles import views as profile_views

app_name = 'accounts'

urlpatterns = [
    path('signup/', profile_views.SignUp.as_view(), name='signup'),
    path('profile/', profile_views.update_profile, name='profile'),
    path('my-favourites/', profile_views.FavouriteListView.as_view(), name='favourites'),
]
