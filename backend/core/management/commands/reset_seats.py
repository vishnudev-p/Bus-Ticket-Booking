from django.core.management.base import BaseCommand
from core.models import Seat

class Command(BaseCommand):
    help = 'Reset all seats to not booked (for testing purposes)'

    def handle(self, *args, **options):
        self.stdout.write("Resetting all seats to not booked...")
        
        # Reset all seats to not booked
        updated_count = Seat.objects.filter(is_booked=True).update(is_booked=False)
        
        self.stdout.write(f"Reset {updated_count} seats to not booked")
        self.stdout.write(self.style.SUCCESS("All seats are now available!")) 