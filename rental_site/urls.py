from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
]

#Add URL maps to redirect the base URL to catalog application
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/')),
]

# Static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#Add Django site authentication urls (for login, logout, password management)
from django.contrib.auth import views as auth_views

urlpatterns += [
    path(r'^login/$', auth_views.login, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include("accounts.urls", namespace="accounts")),

]

''' URL mamgings for accounts
accounts/ login/ [name='login']
accounts/ logout/ [name='logout']
accounts/ password_change/ [name='password_change']
accounts/ password_change/done/ [name='password_change_done']
accounts/ password_reset/ [name='password_reset']
accounts/ password_reset/done/ [name='password_reset_done']
accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/ reset/done/ [name='password_reset_complete']
'''
