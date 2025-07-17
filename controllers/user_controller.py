from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.models import db, ParkingLot, ParkingSpot, Reservation
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/dashboard')
@login_required
def dashboard():
    lots = ParkingLot.query.all()
    reservations = Reservation.query.filter_by(user_id=current_user.id).order_by(Reservation.id.desc()).all()
    return render_template('user_dashboard.html', lots=lots, reservations=reservations)


@user_bp.route('/reserve/<int:lot_id>')
@login_required
def reserve_spot(lot_id):
    available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not available_spot:
        flash("❌ No available spots in this lot.", "danger")
        return redirect(url_for('user.dashboard'))
        return self.duration.total_seconds() / 3600 * self.spot.lot.price_per_hour
    


    # Mark as reserved (still status A)
    reservation = Reservation(spot_id=available_spot.id, user_id=current_user.id)
    db.session.add(reservation)
    db.session.commit()
    flash(f"✅ Spot reserved (ID: {available_spot.id})", "success")
    return redirect(url_for('user.dashboard'))


@user_bp.route('/occupy/<int:reservation_id>')
@login_required
def occupy_spot(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    reservation.start_time = datetime.now()
    reservation.spot.status = 'O'
    db.session.commit()
    flash("🚗 Spot occupied", "info")
    return redirect(url_for('user.dashboard'))


@user_bp.route('/release/<int:reservation_id>')
@login_required
def release_spot(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    reservation.end_time = datetime.now()
    reservation.spot.status = 'A'
    db.session.commit()
    flash("✅ Spot released", "info")
    return redirect(url_for('user.dashboard'))

@user_bp.route('/dashboard')
@login_required
def dashboard():
    lots = ParkingLot.query.all()
    reservations = Reservation.query.filter_by(user_id=current_user.id).order_by(Reservation.id.desc()).all()

    # Chart data: parking dates
    chart_data = [
        r.start_time.strftime('%Y-%m-%d') for r in reservations if r.start_time
    ]

    return render_template('user_dashboard.html', lots=lots, reservations=reservations, chart_data=chart_data)
    flash("✅ Parking lot deleted", "success")
