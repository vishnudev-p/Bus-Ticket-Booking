# Backend (Django) Technical Interview Q&A

## 1. What is the main architecture of the backend?
- The backend is built with Django and Django REST Framework. It uses a modular app structure, with the main logic in the `core` app. The API is RESTful, exposing endpoints for authentication, bus search, seat management, and bookings.

## 2. How is authentication handled?
- JWT (JSON Web Token) authentication is used. Users obtain tokens via `/api/token/` and use them for authenticated requests. Token refresh is supported via `/api/token/refresh/`.

## 3. How are models structured?
- The main models are: `City`, `BusOperator`, `Bus`, `Route`, `Seat`, `Booking`, `Passenger`, and `UserProfile`. Each model represents a real-world entity in the bus booking domain.

## 4. How does the booking process work?
- When a booking is made, the backend validates that the selected seats belong to the correct bus and are not already booked. It creates a `Booking` object, associates the seats and passengers, and marks the seats as booked.

## 5. How is seat availability managed?
- Each `Seat` has an `is_booked` field. When a booking is confirmed, the relevant seats are marked as booked. Management commands are provided to fix or reset seat booking status if needed.

## 6. How are API endpoints organized?
- Endpoints are grouped by resource (cities, routes, buses, seats, bookings). ViewSets and routers are used for standard CRUD operations. Custom actions (like search and cancel) are implemented as needed.

## 7. How is data validation handled?
- Serializers validate input data, including custom validation for seat selection, passenger details, and total fare. Errors are returned with clear messages for the frontend to display.

## 8. How is the admin interface used?
- Django’s admin panel is enabled for managing users, buses, routes, bookings, and more. Admins can add/edit/delete data and monitor bookings.

## 9. How is CORS handled?
- The `django-cors-headers` package is used to allow cross-origin requests from the frontend (React app).

## 10. How are migrations managed?
- Django’s migration system is used. Developers run `makemigrations` and `migrate` to update the database schema as models change.

## 11. How is error handling managed?
- API errors are returned with appropriate HTTP status codes and messages. Validation errors are detailed for easier debugging.

## 12. How is the database seeded with sample data?
- A script in `core/scripts/seed_south_india_data.py` creates sample cities, operators, buses, routes, and seats for testing and demo purposes.

## 13. How are management commands used?
- Custom management commands (`fix_seats`, `reset_seats`) are provided to maintain seat booking consistency and reset seat status for testing.

## 14. How is user data protected?
- Passwords are hashed using Django’s built-in user model. Sensitive endpoints require authentication. Only the booking owner can view/cancel their bookings.

## 15. What are some best practices followed?
- Modular code organization, use of serializers for validation, clear API design, use of transactions for booking, and admin tools for data management.

---

*This file can be expanded with more Q&A as needed for interviews or onboarding.* 