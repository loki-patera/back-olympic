from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Offer
from booking.models import BookingLine

@staff_member_required
def stats(request):
    
  offers = Offer.objects.all()
  stats = []

  for offer in offers:
    count = BookingLine.objects.filter(offer=offer).count()
    stats.append({'offer': offer, 'count': count})

  context = {
    'stats': stats
  }

  return render(request, "offer/stats.html", context)