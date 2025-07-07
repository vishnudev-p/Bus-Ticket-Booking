from django.contrib import admin
from .models import City, BusOperator, Bus, Route, Seat, Booking, Passenger, UserProfile

admin.site.register(City)
admin.site.register(BusOperator)
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Seat)
admin.site.register(Booking)
admin.site.register(Passenger)
admin.site.register(UserProfile)