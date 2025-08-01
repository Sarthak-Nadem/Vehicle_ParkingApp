from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.models import db, ParkingLot, ParkingSpot, User, Reservation

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    lots = ParkingLot.query.all()
    users = User.query.all()
    total_spots = ParkingSpot.query.count()
    occupied = ParkingSpot.query.filter_by(status='O').count()
    available = total_spots - occupied

    return render_template('admin_dashboard.html', lots=lots, users=users, occupied=occupied, available=available)


@admin_bp.route('/create_lot', methods=['GET', 'POST'])
@login_required
def create_lot():
    if request.method == 'POST':
        name = request.form['name'].strip()
        address = request.form['address'].strip()
        pincode = request.form['pincode'].strip()
        price = request.form['price'].strip()
        max_spots = request.form['max_spots'].strip()

        if not (name and address and pincode.isdigit() and price and max_spots.isdigit()):
            flash("invalid input. Please check all fields.", "danger")
            return redirect(url_for('admin.create_lot'))

        lot = ParkingLot(
            name=name,
            address=address,
            pincode=pincode,
            price_per_hour=float(price),
            max_spots=int(max_spots)
        )
        db.session.add(lot)
        db.session.commit()

        # Auto-create parking spots
        for _ in range(int(max_spots)):
            db.session.add(ParkingSpot(lot_id=lot.id, status='A'))

        db.session.commit()
        flash("parking lot created with spots.", "success")
        return redirect(url_for('admin.dashboard'))

    return render_template('create_lot.html')


@admin_bp.route('/expire_stale_reservations')
def expire_stale_reservations():
    from datetime import datetime, timedelta

    cutoff = datetime.utcnow() - timedelta(minutes=30)
    stale_reservations = Reservation.query.filter(
        Reservation.start_time == None,
        Reservation.created_at < cutoff
    ).all()

    count = 0
    for r in stale_reservations:
        r.spot.status = 'A'
        db.session.delete(r)
        count += 1

    db.session.commit()
    flash(f"{count} stale reservations expired and spots released.", "info")
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/delete_lot/<int:lot_id>')
@login_required
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()

    if any(s.status == 'O' for s in spots):
        flash("cannot delete lot. Some spots are still occupied.", "danger")
        return redirect(url_for('admin.dashboard'))

    for s in spots:
        db.session.delete(s)
    db.session.delete(lot)
    db.session.commit()

    flash("parking lot deleted.", "info")
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/reservations')
@login_required
def all_reservations():
    reservations = Reservation.query.order_by(Reservation.id.desc()).all()
    return render_template('admin_reservations.html', reservations=reservations)


@admin_bp.route('/search')
@login_required
def search():
    query = request.args.get('q', '').strip().lower()
    user_results = []
    spot_result = None

    if query:
        user_results = User.query.filter(
            (User.email.ilike(f"%{query}%")) | (User.full_name.ilike(f"%{query}%"))
        ).all()

        if query.isdigit():
            spot_result = ParkingSpot.query.get(int(query))

    return render_template('admin_search.html', query=query, user_results=user_results, spot=spot_result)
