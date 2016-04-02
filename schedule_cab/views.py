from schedule_cab.models import Schedules
from rest_framework import viewsets, exceptions
from schedule_cab.serializers import SchedulesSerializer
from rest_framework.decorators import api_view
from schedule_cab.utils import get_uber_products
from rest_framework.response import Response
from rest_framework import status


class SchedulesListViewSet(viewsets.ModelViewSet):
    """
    API endpoint to schedule cab
    """
    queryset = Schedules.objects.all().order_by('-schedule_time')
    serializer_class = SchedulesSerializer

    def create(self, request):
        data = super(SchedulesListViewSet, self).create(request)
        return Response(
            {'detail': 'Cab booked successfully'},
            status=status.HTTP_201_CREATED
        )


@api_view(('GET',))
def uber_products(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    if not all([latitude, longitude]):
        raise exceptions.ParseError('Latitude and longitude are mandatory fields.')
    products = get_uber_products(latitude, longitude)
    if products is None:
        raise exceptions.APIException('Service temporarily unavailable, try again later.')

    return Response(products)
