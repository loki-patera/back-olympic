from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Booking, BookingLine
from .serializers import PaymentSerializer
from event.models import Event
from offer.models import Offer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_payment(request: Request) -> Response:

  serializer = PaymentSerializer(data=request.data)

  if not serializer.is_valid():
    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
  
  cart = serializer.validated_data['cart']

  with transaction.atomic():

    booking = Booking.objects.create(person=request.user)

    for item in cart:

      event = Event.objects.get(pk=item['id_event'])
      offer = Offer.objects.get(pk=item['id_offer'])

      BookingLine.objects.create(
        booking=booking,
        event=event,
        offer=offer
      )
  
    return Response({"success": True}, status=status.HTTP_201_CREATED)