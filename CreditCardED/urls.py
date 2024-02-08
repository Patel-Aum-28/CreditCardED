from django.contrib import admin
from django.urls import include, path, re_path
from django.shortcuts import redirect

admin.site.site_header = 'CreditCardED Administration'
admin.site.site_title = 'Admin Panel'
admin.site.index_title = 'Admin Panel'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('client/', include('client.urls')),
    path('server/', include('server.urls')),
    path('server/', lambda request: redirect('encrypted-data/')),
    path('client/', lambda request: redirect('payment/')),
    path('', lambda request: redirect('client/payment/')),
]
