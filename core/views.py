from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PlatformStats

@api_view(["GET"])
def stats(request):
    rows = PlatformStats.objects.all().order_by("platform")
    return Response({
        "total_solved": rows.aggregate(t=Sum("solved"))["t"] or 0,
        "platforms": [
            {"platform": r.platform, "handle": r.handle, "rating": r.rating,
             "max_rating": r.max_rating, "solved": r.solved,
             "url": r.profile_url, "updated_at": r.updated_at}
            for r in rows
        ],
    })