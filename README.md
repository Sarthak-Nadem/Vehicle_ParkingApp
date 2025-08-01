# 🚗 Vehicle Parking App - MAD-I

This is a multi-user web application built as part of the *Modern Application Development I* course. The app allows 4-wheeler users to book and release parking spots while providing full parking lot and user management capabilities to admins.

## 🔑 Features

### 👤 User
- Register and login securely
- View all parking lots and spot availability
- Reserve a spot, mark as occupied, and release it
- View reservation history and cost summary
- Chart-based reservation timeline
- Smart locking with expiration for inactive reservations

### 🛠️ Admin
- Secure login with username/password
- Create and delete parking lots
- View all users and their reservation history
- Search users and spot IDs
- Doughnut chart of occupied vs available spots

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
- [x] API access for spots, lots
- [x] Charts and admin summaries
- [x] Frontend + Backend validations

## 🚀 Running the App

1. Clone the repo:
   ```bash
   git clone https://github.com/24f2003400/Vehicle_ParkingApp-V1
   cd vehicle-parking-app
