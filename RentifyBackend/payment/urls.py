# payment/urls.py
from django.urls import path

from payment.views import CreatePaymentView, VerifyPaymentView

urlpatterns = [
    path("api/payment/create/", CreatePaymentView.as_view(), name="create-payment"),
    path("api/payment/verify/", VerifyPaymentView.as_view(), name="verify-payment"),
]
