from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from azbankgateways.exceptions import AZBankGatewaysException
from .models import Payment
from reservation.models import Reservation


def create_payment(request, reservation_id, mobile_number=None):
    """
    ایجاد پرداخت برای رزرو مشخص
    """
    try:
        reservation = Reservation.objects.get(id=reservation_id, user=request.user)
    except Reservation.DoesNotExist:
        return None, None

    amount = int(round(reservation.total_price))

    factory = bankfactories.BankFactory()
    try:
        bank = factory.create(bank_models.BankType.ZARINPAL)
        bank.set_request(request)
        bank.set_amount(amount)
        bank.set_client_callback_url(reverse('verify-payment'))
        if mobile_number:
            bank.set_mobile_number(mobile_number)

        bank_record = bank.ready()
        payment = Payment.objects.create(
            user=request.user,
            reservation=reservation,
            amount=amount,
            authority=bank_record.reference_number,
            ref_id=bank_record.tracking_code,
            status='pending'
        )

        payment_url = bank.get_gateway()["url"]
        return payment, payment_url
    except AZBankGatewaysException:
        return None, None


def verify_payment(request):
    """
    تایید پرداخت بعد از بازگشت از بانک
    """
    print(request.GET)
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    if not authority or status != 'OK':
        return None

    try:
        payment = Payment.objects.get(authority=authority, status='pending')
    except Payment.DoesNotExist:
        return None

    factory = bankfactories.BankFactory()
    bank = factory.create(bank_models.BankType.ZARINPAL)
    bank.set_request(request)

    try:
        bank.verify(payment.ref_id)

        payment.status = 'success'
        payment.ref_id = bank.get_tracking_code()
        payment.save()

        # می‌تونی اینجا رزرو رو هم confirm کنی
        reservation = payment.reservation
        reservation.status = 'confirmed'
        reservation.save()

        return payment

    except AZBankGatewaysException:
        payment.status = 'failed'
        payment.save()
        return None
