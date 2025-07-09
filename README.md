# 🚗 Vehicle Parking App - MAD-I

This is a multi-user web application built as part of the *Modern Application Development I* course. The app allows 4-wheeler users to book and release parking spots while providing full parking lot and user management capabilities to admins.

## 👥 Roles
- **Admin**: Can manage parking lots and view all users and reservations. No registration required.
- **User**: Can register, log in, book a spot, view history, and release it.

## 🧰 Tech Stack

| Layer         | Technology                          |
|---------------|--------------------------------------|
| Backend       | Flask, Flask-SQLAlchemy              |
| Frontend      | HTML, CSS, Bootstrap, Jinja2         |
| Database      | SQLite (Programmatically created)    |
| Auth & Login  | Flask-Login                          |
| Visualization | Chart.js (planned)                   |
| Others        | Python 3.12+, Git                    |

## 🔧 Features (Planned Milestones)

- [x] Admin and User role-based login
- [x] Parking lot and spot management
- [x] Auto-allocation of spots
- [x] Timestamp and cost tracking
- [x] Reservation history
- [ ] API access for spots, lots
- [ ] Charts and admin summaries
- [ ] Frontend + Backend validations

## 🚀 Running the App

1. Clone the repo:
   ```bash
   git clone https://github.com/24f2003400/Vehicle_ParkingApp-V1
   cd vehicle-parking-app
