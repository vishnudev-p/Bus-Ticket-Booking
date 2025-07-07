from core.models import City, BusOperator, Bus, Route, Seat; from django.contrib.auth.models import User; from datetime import datetime, timedelta; from decimal import Decimal

city_objs = {name: City.objects.get_or_create(name=name)[0] for name in ['Bangalore','Chennai','Hyderabad','Kochi','Trivandrum','Coimbatore','Mysore','Mangalore','Madurai','Vijayawada','Tirupati','Pondicherry','Salem','Erode','Calicut','Hubli','Belgaum']}

operator_objs = {name: BusOperator.objects.get_or_create(name=name, defaults={'contact_email': f'{name.replace(" ","").lower()}@mail.com', 'phone': '9876543210'})[0] for name in ['KPN Travels', 'SRS Travels', 'VRL', 'Parveen', 'Kallada', 'Orange Travels']}

bus_data = [('B001', 'KPN Travels', 'AC', 40, 4.5), ('B002', 'SRS Travels', 'Non-AC', 60, 4.2), ('B003', 'VRL', 'Sleeper', 40, 4.7), ('B004', 'Parveen', 'Seater', 50, 4.0), ('B005', 'Kallada', 'AC', 40, 4.3), ('B006', 'Orange Travels', 'Sleeper', 40, 4.6)]

bus_objs = {bus_number: Bus.objects.get_or_create(bus_number=bus_number, defaults={'operator': operator_objs[op], 'bus_type': bus_type, 'total_seats': total_seats, 'rating': rating})[0] for bus_number, op, bus_type, total_seats, rating in bus_data}

routes_data = [('Bangalore', 'Chennai', 'B001', 20, 7, 800), ('Chennai', 'Hyderabad', 'B003', 21, 10, 1200), ('Kochi', 'Bangalore', 'B002', 18, 10, 950), ('Hyderabad', 'Bangalore', 'B005', 19, 9, 1100), ('Mysore', 'Chennai', 'B004', 22, 8, 900), ('Trivandrum', 'Kochi', 'B006', 17, 5, 600)]

route_objs = {(src, dst, bus): Route.objects.get_or_create(source=city_objs[src], destination=city_objs[dst], bus=bus_objs[bus], departure_time=datetime.now().replace(hour=dep, minute=0, second=0, microsecond=0)+timedelta(days=1), arrival_time=datetime.now().replace(hour=dep, minute=0, second=0, microsecond=0)+timedelta(days=1)+timedelta(hours=dur), defaults={'fare': Decimal(fare)})[0] for src, dst, bus, dep, dur, fare in routes_data}

[Seat.objects.get_or_create(bus=bus, seat_number=str(i), defaults={'is_booked': False}) for bus in bus_objs.values() for i in range(1, bus.total_seats+1)]

print("South India sample data seeded successfully!")
