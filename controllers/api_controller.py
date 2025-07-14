from flask import Blueprint, jsonify
from models.models import db, ParkingLot, ParkingSpot, Reservation, User

api_bp = Blueprint('api', __name__, url_prefix='/api')

# ---- Get All Parking Lots ----
@api_bp.route('/lots')
def get_lots():
    lots = ParkingLot.query.all()
    return jsonify([
        {
            "id": lot.id,
            "name": lot.name,
            "address": lot.address,
            "pincode": lot.pincode,
            "price_per_hour": lot.price_per_hour,
            "max_spots": lot.max_spots
        } for lot in lots
    ])

# ---- Get All Parking Spots ----
@api_bp.route('/spots')
def get_spots():
    spots = ParkingSpot.query.all()
    return jsonify([
        {
            "id": spot.id,
            "lot_id": spot.lot_id,
            "status": spot.status
        } for spot in spots
    ])

# ---- Get All Reservations ----
@api_bp.route('/reservations')
def get_reservations():
    reservations = Reservation.query.all()
    return jsonify([
        {
            "id": r.id,
            "spot_id": r.spot_id,
            "user_id": r.user_id,
            "start_time": r.start_time.isoformat() if r.start_time else None,
            "end_time": r.end_time.isoformat() if r.end_time else None,
            "total_cost": r.total_cost
        } for r in reservations
    ])

# ---- Get All Users (Admin-only Use) ----
@api_bp.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([
        {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        } for user in users
    ])
