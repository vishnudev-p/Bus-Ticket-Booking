from rest_framework import serializers
from .models import City, BusOperator, Bus, Route, Seat, Booking, Passenger, UserProfile
from django.contrib.auth.models import User

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

class BusOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusOperator
        fields = ['id', 'name', 'contact_email', 'phone']

class BusSerializer(serializers.ModelSerializer):
    operator = BusOperatorSerializer(read_only=True)
    class Meta:
        model = Bus
        fields = ['id', 'operator', 'bus_number', 'bus_type', 'total_seats', 'rating']

class RouteSerializer(serializers.ModelSerializer):
    source = CitySerializer(read_only=True)
    destination = CitySerializer(read_only=True)
    bus = BusSerializer(read_only=True)
    class Meta:
        model = Route
        fields = ['id', 'source', 'destination', 'bus', 'departure_time', 'arrival_time', 'fare']

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'bus', 'seat_number', 'is_booked']

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['id', 'name', 'age', 'gender']

    def validate(self, data):
        print(f"Passenger validation data: {data}")
        if not isinstance(data.get('age'), int) or data.get('age') <= 0:
            print("ERROR: Invalid age")
            raise serializers.ValidationError({"age": "Age must be a positive integer."})
        if data.get('gender') not in ['Male', 'Female', 'Other']:
            print("ERROR: Invalid gender")
            raise serializers.ValidationError({"gender": "Gender must be Male, Female, or Other."})
        print("Passenger validation passed!")
        return data

class BookingSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)
    passengers = PassengerSerializer(many=True, read_only=True)
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all(), write_only=True)
    route_details = RouteSerializer(source='route', read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'route', 'route_details', 'seats', 'passengers',
            'booking_date', 'total_fare', 'status'
        ]
        read_only_fields = ['user', 'booking_date', 'route_details']

    def validate(self, data):
        print("Received data:", self.initial_data)  # Debug
        
        # Validate that number of passengers matches number of seats
        passengers_data = self.initial_data.get('passengers', [])
        seats_data = self.initial_data.get('seats', [])
        
        print(f"Passengers count: {len(passengers_data)}, Seats count: {len(seats_data)}")
        
        if len(passengers_data) != len(seats_data):
            print("ERROR: Passenger count doesn't match seat count")
            raise serializers.ValidationError("Number of passengers must match number of seats.")
        
        # Validate seats
        route_id = self.initial_data.get('route')
        if not route_id:
            print("ERROR: Route ID is missing")
            raise serializers.ValidationError("Route is required.")
        
        print(f"Route ID: {route_id}")
        route = Route.objects.filter(id=route_id).first()
        if not route:
            print("ERROR: Invalid route ID")
            raise serializers.ValidationError("Invalid route ID.")
        
        print(f"Route found: {route}")
        
        # Get seat objects and validate them
        seats = Seat.objects.filter(id__in=seats_data)
        print(f"Seats found: {seats.count()}, Seats requested: {len(seats_data)}")
        print(f"Seat IDs requested: {seats_data}")
        print(f"Seat IDs found: {list(seats.values_list('id', flat=True))}")
        
        if len(seats) != len(seats_data):
            print("ERROR: Some seat IDs are invalid")
            raise serializers.ValidationError("Some seat IDs are invalid.")
        
        print(f"Route bus: {route.bus}, Seat buses: {[seat.bus for seat in seats]}")
        if not all(seat.bus == route.bus for seat in seats):
            print("ERROR: Some seats do not belong to the route's bus")
            raise serializers.ValidationError("Some seats do not belong to the route's bus.")
        
        print(f"Seats booked status: {[seat.is_booked for seat in seats]}")
        if not all(not seat.is_booked for seat in seats):
            print("ERROR: Some seats are already booked")
            raise serializers.ValidationError("Some seats are already booked.")
        
        print("All validations passed!")
        return super().validate(data)

    def validate_total_fare(self, value):
        print("Total fare received:", value, "Type:", type(value))  # Debug
        print("Total fare raw value:", repr(value))  # Debug - show exact value
        
        # Handle None or empty values
        if value is None or value == '':
            raise serializers.ValidationError("Total fare is required.")
        
        try:
            # Convert to Decimal for proper handling
            from decimal import Decimal, InvalidOperation
            
            if isinstance(value, str):
                value = Decimal(value.strip())
            elif isinstance(value, (int, float)):
                value = Decimal(str(value))
            else:
                # Try to convert any other type
                value = Decimal(str(value))
            
            print("Total fare after conversion:", value, "Type:", type(value))  # Debug
            
            if value <= 0:
                raise serializers.ValidationError("Total fare must be a positive number.")
            
            return value
        except (ValueError, TypeError, AttributeError, InvalidOperation) as e:
            print("Total fare validation error:", str(e))  # Debug
            raise serializers.ValidationError(f"Total fare must be a valid number. Received: {repr(value)}")

    def create(self, validated_data):
        print("Starting booking creation...")
        # Get passengers and seats data from initial_data since they're read_only in validated_data
        passengers_data = self.initial_data.get('passengers', [])
        seats_data = self.initial_data.get('seats', [])
        
        print(f"Passengers data: {passengers_data}")
        print(f"Seats data: {seats_data}")
        print(f"Validated data: {validated_data}")
        
        # Use database transaction to ensure atomicity
        from django.db import transaction
        
        with transaction.atomic():
            # Double-check that seats are still available
            seats = Seat.objects.filter(id__in=seats_data, is_booked=False)
            print(f"Available seats found: {seats.count()}")
            if len(seats) != len(seats_data):
                print("ERROR: Some seats are no longer available")
                raise serializers.ValidationError("Some seats are no longer available.")
            
            # Create the booking without seats (we'll add them after)
            booking = Booking.objects.create(**validated_data)
            print(f"Booking created with ID: {booking.id}")
            
            # Create passengers
            for passenger_data in passengers_data:
                print(f"Creating passenger: {passenger_data}")
                Passenger.objects.create(booking=booking, **passenger_data)
            
            # Set seats for the booking
            booking.seats.set(seats)
            print(f"Seats set for booking: {list(seats.values_list('id', flat=True))}")
            
            # Mark seats as booked
            for seat in seats:
                seat.is_booked = True
                seat.save()
            print("Seats marked as booked")
        # Fetch the booking with all related fields for full serialization
        booking = Booking.objects.prefetch_related('seats', 'passengers').select_related('route__source', 'route__destination', 'route__bus__operator').get(id=booking.id)
        print("Booking creation completed successfully!")
        return booking

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'phone', 'address']