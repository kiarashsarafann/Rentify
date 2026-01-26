from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .services import create_payment, verify_payment

from reservation.models import Reservation


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # گرفتن آخرین رزرو کاربر لاگین‌شده
        try:
            reservation = Reservation.objects.filter(user=request.user, status='pending').latest('created_at')
        except Reservation.DoesNotExist:
            return Response({"error": "No pending reservation found"}, status=status.HTTP_404_NOT_FOUND)

        # گرفتن قیمت نهایی رزرو
        mobile = getattr(request.user, 'phone_number', None)  # اگر کاربر شماره موبایل دارد

        # ایجاد پرداخت
        payment, payment_url = create_payment(request, reservation.id, mobile_number=mobile)
        if payment_url:
            return Response({
                "payment_id": payment.id,
                "payment_url": payment_url,
                "reservation_id": reservation.id,
                "amount": payment.amount,
                "status": payment.status,
            })

        return Response({"error": "Payment creation failed"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyPaymentView(APIView):
    def get(self, request):
        payment = verify_payment(request)

        if not payment:
            return Response(
                {"error": "Payment verification failed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "status": payment.status,
            "amount": payment.amount,
            "ref_id": payment.ref_id,
            "reservation_id": payment.reservation.id
        })
