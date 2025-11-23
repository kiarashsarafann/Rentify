from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    AddCartItemSerializer,
    RemoveCartItemSerializer,
)


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: CartSerializer})
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AddCartItemSerializer)
    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart, created = Cart.objects.get_or_create(user=request.user)

        item = CartItem.objects.create(
            cart=cart,
            vehicle=serializer.validated_data["vehicle"],
            start_time=serializer.validated_data["start_time"],
            end_time=serializer.validated_data["end_time"],
        )

        return Response({
            "message": "آیتم با موفقیت اضافه شد",
            "item_id": item.id
        }, status=status.HTTP_201_CREATED)


class RemoveCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=RemoveCartItemSerializer)
    def delete(self, request):
        serializer = RemoveCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item_id = serializer.validated_data["item_id"]

        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
            item.delete()
            return Response({"message": "آیتم حذف شد"})
        except CartItem.DoesNotExist:
            return Response(
                {"error": "آیتم پیدا نشد"},
                status=status.HTTP_404_NOT_FOUND
            )
