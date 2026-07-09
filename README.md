# Hostel Booking System

This is my Flask project for managing hostel bookings. I built this as a simple REST API where you can add hostels, add rooms to those hostels, and let guests book rooms. It also handles cancelling bookings and freeing up the room again.

## What I used
- Python (Flask)
- Flask-SQLAlchemy for the database
- SQLite (just a local file, no need to install anything extra)

# How to run it

1. Clone this repo
2. Make a virtual environment so packages don't mess with your system Python

## Auth 
- POST /register → create a new user account
- POST /login → log in (creates a session/cookie)
- POST /logout → log out (clears the session)
- GET /session → check if you're currently logged in