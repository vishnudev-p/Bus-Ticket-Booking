from rest_framework import viewsets, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import City, BusOperator, Bus, Route, Seat, Booking
from .serializers import CitySerializer, BusOperatorSerializer, BusSerializer, RouteSerializer, SeatSerializer, BookingSerializer, UserSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

class BusOperatorViewSet(viewsets.ModelViewSet):
    queryset = BusOperator.objects.all()
    serializer_class = BusOperatorSerializer
    permission_classes = [AllowAny]

class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [AllowAny]

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [AllowAny]  # Allow search without authentication
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['source', 'destination', 'bus__bus_type', 'fare']
    ordering_fields = ['fare', 'departure_time', 'bus__rating']

    @action(detail=False, methods=['get'])
    def search(self, request):
        source = request.query_params.get('source')
        destination = request.query_params.get('destination')
        date = request.query_params.get('date')
        queryset = self.get_queryset()
        if source and destination and date:
            try:
                date = datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(
                    source__id=source,
                    destination__id=destination,
                    departure_time__date=date
                )
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [AllowAny]  # Allow seat viewing without authentication
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bus', 'is_booked']

    def get_queryset(self):
        queryset = Seat.objects.all()
        bus_id = self.request.query_params.get('bus_id')
        if bus_id:
            queryset = queryset.filter(bus__id=bus_id)
        return queryset

    @action(detail=False, methods=['get'])
    def available_seats(self, request):
        bus_id = request.query_params.get('bus_id')
        if bus_id:
            queryset = self.get_queryset().filter(bus__id=bus_id, is_booked=False)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"error": "Bus ID required."}, status=400)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # Restrict to logged-in users

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Use authenticated user

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status != 'Confirmed':
            return Response({'error': 'Only confirmed bookings can be cancelled.'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'Cancelled'
        booking.save()
        # Mark all associated seats as available
        for seat in booking.seats.all():
            seat.is_booked = False
            seat.save()
        return Response({'success': 'Booking cancelled successfully.'}, status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.userprofile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.userprofile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)