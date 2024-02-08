from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from . import views
from .views import encrypted_data_list, decrypt_data_view

app_name = 'server'

urlpatterns = [
    path('encrypted-data/', views.encrypted_data_list, name='encrypted_data_list'),
    path('decrypt/<str:encrypted_data_id>/', views.decrypt_data_view, name='decrypt_data_view'),
]
