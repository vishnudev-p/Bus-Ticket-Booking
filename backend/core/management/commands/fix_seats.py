from django.core.management.base import BaseCommand
from core.models import Seat, Booking
from django.db import transaction

class Command(BaseCommand):
    help = 'Fix seat booking status by ensuring only seats that are actually booked by users are marked as booked'

    def handle(self, *args, **options):
        self.stdout.write("Checking and fixing seat booking status...")
        
        # Get all seats that are marked as booked
        booked_seats = Seat.objects.filter(is_booked=True)
        self.stdout.write(f"Found {booked_seats.count()} seats marked as booked")
        
        # Get all actual bookings
        actual_bookings = Booking.objects.all()
        self.stdout.write(f"Found {actual_bookings.count()} actual bookings")
        
        # Get all seats that are actually booked by users
        actually_booked_seat_ids = set()
        for booking in actual_bookings:
            for seat in booking.seats.all():
                actually_booked_seat_ids.add(seat.id)
        
        self.stdout.write(f"Seats actually booked by users: {len(actually_booked_seat_ids)}")
        
        # Fix seats that are marked as booked but not actually booked
        with transaction.atomic():
            for seat in booked_seats:
                if seat.id not in actually_booked_seat_ids:
                    self.stdout.write(f"Fixing seat {seat.id} (Bus: {seat.bus.bus_number}, Seat: {seat.seat_number}) - marked as booked but not actually booked")
                    seat.is_booked = False
                    seat.save()
        
        # Double check - mark seats as booked if they are actually booked
        for booking in actual_bookings:
            for seat in booking.seats.all():
                if not seat.is_booked:
                    self.stdout.write(f"Fixing seat {seat.id} (Bus: {seat.bus.bus_number}, Seat: {seat.seat_number}) - actually booked but not marked as booked")
                    seat.is_booked = True
                    seat.save()
        
        # Final count
        final_booked_seats = Seat.objects.filter(is_booked=True).count()
        self.stdout.write(f"Final count of seats marked as booked: {final_booked_seats}")
        self.stdout.write(self.style.SUCCESS("Seat booking status fixed!")) 