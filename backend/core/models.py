from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class BusOperator(models.Model):
    name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name

class Bus(models.Model):
    BUS_TYPES = (
        ('AC', 'AC'),
        ('Non-AC', 'Non-AC'),
        ('Sleeper', 'Sleeper'),
        ('Seater', 'Seater'),
    )
    operator = models.ForeignKey(BusOperator, on_delete=models.CASCADE)
    bus_number = models.CharField(max_length=50, unique=True)
    bus_type = models.CharField(max_length=10, choices=BUS_TYPES)
    total_seats = models.PositiveIntegerField()
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.bus_number} ({self.bus_type})"

class Route(models.Model):
    source = models.ForeignKey(City, related_name='source_routes', on_delete=models.CASCADE)
    destination = models.ForeignKey(City, related_name='destination_routes', on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    fare = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.source} to {self.destination} - {self.bus}"

class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ['bus', 'seat_number']

    def __str__(self):
        return f"{self.bus.bus_number} - Seat {self.seat_number}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    booking_date = models.DateTimeField(auto_now_add=True)
    total_fare = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Confirmed')

    def __str__(self):
        return f"Booking {self.id} by {self.user.username}"

class Passenger(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers')
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')))

    def __str__(self):
        return f"{self.name} (Booking {self.booking.id})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"