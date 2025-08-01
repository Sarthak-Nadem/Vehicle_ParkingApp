from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.models import db, ParkingLot, ParkingSpot, Reservation
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/dashboard')
@login_required
def dashboard():
    lots = ParkingLot.query.all()
    reservations = Reservation.query.filter_by(user_id=current_user.id).order_by(Reservation.id.desc()).all()

    chart_data = [
        r.start_time.strftime('%Y-%m-%d') for r in reservations if r.start_time
    ]

    return render_template('user_dashboard.html', lots=lots, reservations=reservations, chart_data=chart_data)


@user_bp.route('/reserve/<int:lot_id>')
@login_required
def reserve_spot(lot_id):
    available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not available_spot:
        flash("No available spots in this lot.", "danger")
        return redirect(url_for('user.dashboard'))

    available_spot.status = 'R'  # New status for 'Reserved'

    reservation = Reservation(spot_id=available_spot.id, user_id=current_user.id)
    db.session.add(reservation)
    db.session.commit()

    flash(f"Spot reserved (ID: {available_spot.id})", "success")
    return redirect(url_for('user.dashboard'))



@user_bp.route('/occupy/<int:reservation_id>')
@login_required
def occupy_spot(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    if reservation.spot.status == 'O':
        flash("This spot is already occupied by someone else.", "danger")
        return redirect(url_for('user.dashboard'))
    reservation.start_time = datetime.now()
    reservation.spot.status = 'O'
    db.session.commit()

    flash("🚗 Spot marked as occupied.", "info")
    return redirect(url_for('user.dashboard'))
