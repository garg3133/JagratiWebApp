from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'payment'
urlpatterns = [
    path('paytm/', csrf_exempt(views.payment), name="payment"),
    path('handler/', csrf_exempt(views.payment_handler), name="payment_handler"),
    path('invoice', views.invoice, name='invoice'),
]
