# Database (SQLite3) Technical Interview Q&A

## 1. Why was SQLite3 chosen for this project?
- SQLite3 is lightweight, serverless, and easy to set up for development and testing. It requires no separate server process and is included with Python, making it ideal for rapid prototyping.

## 2. How does Django interact with SQLite3?
- Django uses its ORM (Object-Relational Mapping) to interact with SQLite3. Models are defined in Python, and Django translates queries to SQL under the hood.

## 3. What are the main tables in the database?
- The main tables correspond to Django models: `auth_user`, `core_city`, `core_busoperator`, `core_bus`, `core_route`, `core_seat`, `core_booking`, `core_passenger`, and `core_userprofile`.

## 4. How are relationships managed in the schema?
- Foreign keys and many-to-many relationships are used. For example, `core_seat` has a foreign key to `core_bus`, and `core_booking` has a many-to-many relationship with `core_seat`.

## 5. How are migrations handled?
- Django’s migration system creates and updates the SQLite schema as models change. Commands like `makemigrations` and `migrate` are used to apply changes.

## 6. How is data integrity ensured?
- Django enforces field types, unique constraints, and foreign key relationships at the ORM level. The database also enforces these constraints.

## 7. How are seats and bookings linked?
- The `core_booking_seats` table links bookings to seats (many-to-many). Each seat also has an `is_booked` flag for quick availability checks.

## 8. How can you inspect the SQLite database?
- You can use the `sqlite3` command-line tool or GUI tools like DB Browser for SQLite to view and query the database file (`db.sqlite3`).

## 9. How do you reset or seed the database?
- You can delete `db.sqlite3` and rerun migrations to reset. The provided seed script (`seed_south_india_data.py`) can be run to populate sample data.

## 10. How are transactions used?
- Django uses transactions to ensure atomic operations, especially during booking, to prevent double-booking of seats.

## 11. How are unique constraints enforced?
- The `unique_together` meta option is used in models (e.g., bus and seat_number in `Seat`). SQLite enforces these constraints at the database level.

## 12. How do you handle database performance?
- For development, SQLite is sufficient. For production, switching to PostgreSQL or MySQL is recommended for better performance and concurrency.

## 13. How are migrations tracked?
- The `django_migrations` table tracks which migrations have been applied to the database.

## 14. How do you backup the database?
- Simply copy the `db.sqlite3` file. For more advanced backup, use the `sqlite3` dump command.

## 15. What are some best practices for using SQLite with Django?
- Use SQLite for development and testing, but migrate to a more robust database for production. Always use migrations to manage schema changes, and avoid manual schema edits.

---

*This file can be expanded with more Q&A as needed for interviews or onboarding.* 