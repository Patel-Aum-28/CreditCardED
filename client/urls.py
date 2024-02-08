from django.urls import path
from .views import payment_form

app_name = 'client'

urlpatterns = [
    path('payment/', payment_form, name='payment_form'),
]
