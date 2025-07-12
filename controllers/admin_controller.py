from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.models import db, ParkingLot, ParkingSpot, User, Reservation

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    lots = ParkingLot.query.all()
    users = User.query.all()
    return render_template('admin_dashboard.html', lots=lots, users=users)

@admin_bp.route('/reservations')
@login_required
def all_reservations():
    from models.models import Reservation
    reservations = Reservation.query.order_by(Reservation.start_time.desc()).all()
    return render_template('admin_reservations.html', reservations=reservations)

@admin_bp.route('/create_lot', methods=['GET', 'POST'])
@login_required
def create_lot():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        pincode = request.form['pincode']
        price = float(request.form['price'])
        max_spots = int(request.form['max_spots'])

        lot = ParkingLot(name=name, address=address, pincode=pincode,
                         price_per_hour=price, max_spots=max_spots)
        db.session.add(lot)
        db.session.commit()

        for _ in range(max_spots):
            spot = ParkingSpot(lot_id=lot.id, status='A')
            db.session.add(spot)
        db.session.commit()

        flash("✅ Parking lot created with spots", "success")
        return redirect(url_for('admin.dashboard'))

    return render_template('create_lot.html')


@admin_bp.route('/delete_lot/<int:lot_id>')
@login_required
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()

    if any(s.status == 'O' for s in spots):
        flash("❌ Cannot delete: Some spots are occupied", "danger")
        return redirect(url_for('admin.dashboard'))

    for s in spots:
        db.session.delete(s)
    db.session.delete(lot)
    db.session.commit()

    flash("🗑️ Parking lot deleted", "info")
    return redirect(url_for('admin.dashboard'))
