from core.models import Seat, Booking
from django.db import transaction

def fix_seat_bookings():
    """
    Fix seat booking status by ensuring only seats that are actually booked
    by users are marked as booked.
    """
    print("Checking and fixing seat booking status...")
    
    # Get all seats that are marked as booked
    booked_seats = Seat.objects.filter(is_booked=True)
    print(f"Found {booked_seats.count()} seats marked as booked")
    
    # Get all actual bookings
    actual_bookings = Booking.objects.all()
    print(f"Found {actual_bookings.count()} actual bookings")
    
    # Get all seats that are actually booked by users
    actually_booked_seat_ids = set()
    for booking in actual_bookings:
        for seat in booking.seats.all():
            actually_booked_seat_ids.add(seat.id)
    
    print(f"Seats actually booked by users: {len(actually_booked_seat_ids)}")
    
    # Fix seats that are marked as booked but not actually booked
    with transaction.atomic():
        for seat in booked_seats:
            if seat.id not in actually_booked_seat_ids:
                print(f"Fixing seat {seat.id} (Bus: {seat.bus.bus_number}, Seat: {seat.seat_number}) - marked as booked but not actually booked")
                seat.is_booked = False
                seat.save()
    
    # Double check - mark seats as booked if they are actually booked
    for booking in actual_bookings:
        for seat in booking.seats.all():
            if not seat.is_booked:
                print(f"Fixing seat {seat.id} (Bus: {seat.bus.bus_number}, Seat: {seat.seat_number}) - actually booked but not marked as booked")
                seat.is_booked = True
                seat.save()
    
    # Final count
    final_booked_seats = Seat.objects.filter(is_booked=True).count()
    print(f"Final count of seats marked as booked: {final_booked_seats}")
    print("Seat booking status fixed!")

if __name__ == "__main__":
    fix_seat_bookings() 