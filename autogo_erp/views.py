"""HTTP routes for the AutoGo ERP inventory module.

This blueprint defines endpoints to list, create, edit and delete cars in
the inventory.  For demonstration purposes we provide both HTML
renderings for browser interaction and JSON APIs for programmatic
access.  All routes are namespaced under the blueprint ``bp`` to keep
the application modular.
"""

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from . import db
from .models import Car


# Create a blueprint for the main module
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Redirect to the inventory listing."""
    return redirect(url_for('main.list_cars'))


@bp.route('/cars', methods=['GET'])
def list_cars():
    """List all cars in the inventory.

    Renders an HTML page with a table of cars.  Alternatively,
    requests with an ``Accept: application/json`` header will
    receive a JSON array of car dictionaries.
    """
    cars = Car.query.all()
    # If the client accepts JSON (via fetch or API) return JSON
    if request.accept_mimetypes.best == 'application/json':
        return jsonify([car.to_dict() for car in cars])
    return render_template('list.html', cars=cars)


@bp.route('/cars/new', methods=['GET', 'POST'])
def create_car():
    """Create a new car entry.

    On GET requests this displays a form.  On POST requests it
    processes form data and persists the new car to the database.
    """
    if request.method == 'POST':
        # Extract form fields
        brand = request.form.get('brand', '').strip()
        model_name = request.form.get('model', '').strip()
        year = request.form.get('year', '').strip()
        vin = request.form.get('vin', '').strip()
        color = request.form.get('color', '').strip()
        price = request.form.get('price', '').strip()
        status = request.form.get('status', '').strip() or 'Disponible'
        entry_date_str = request.form.get('entry_date', '').strip()

        # Validate required fields
        errors: list[str] = []
        if not brand:
            errors.append('La marca es obligatoria.')
        if not model_name:
            errors.append('El modelo es obligatorio.')
        if not year or not year.isdigit():
            errors.append('El año debe ser numérico.')
        if not vin:
            errors.append('El VIN es obligatorio.')
        if not color:
            errors.append('El color es obligatorio.')
        if not price:
            errors.append('El precio es obligatorio.')

        # Try to parse date if provided
        entry_date = None
        if entry_date_str:
            try:
                entry_date = datetime.strptime(entry_date_str, '%Y-%m-%d').date()
            except ValueError:
                errors.append('La fecha de ingreso debe tener formato YYYY-MM-DD.')
        else:
            entry_date = datetime.today().date()

        if errors:
            for error in errors:
                flash(error, 'danger')
            # re-render the form with the previously entered values
            return render_template('form.html', car=None, form=request.form)

        # Convert types
        try:
            year_int = int(year)
            price_float = float(price)
        except ValueError:
            flash('Año y precio deben ser numéricos.', 'danger')
            return render_template('form.html', car=None, form=request.form)

        # Check VIN uniqueness
        if Car.query.filter_by(vin=vin).first():
            flash('Ya existe un vehículo con ese VIN.', 'danger')
            return render_template('form.html', car=None, form=request.form)

        # Create and save the car
        car = Car(
            brand=brand,
            model=model_name,
            year=year_int,
            vin=vin,
            color=color,
            price=price_float,
            status=status,
            entry_date=entry_date,
        )
        db.session.add(car)
        db.session.commit()
        flash('Vehículo agregado con éxito.', 'success')
        return redirect(url_for('main.list_cars'))
    # GET request: render empty form
    return render_template('form.html', car=None, form={})


@bp.route('/cars/<int:car_id>/edit', methods=['GET', 'POST'])
def edit_car(car_id: int):
    """Edit an existing car entry."""
    car = Car.query.get_or_404(car_id)
    if request.method == 'POST':
        # Collect updated values from the form
        brand = request.form.get('brand', '').strip()
        model_name = request.form.get('model', '').strip()
        year = request.form.get('year', '').strip()
        vin = request.form.get('vin', '').strip()
        color = request.form.get('color', '').strip()
        price = request.form.get('price', '').strip()
        status = request.form.get('status', '').strip() or 'Disponible'
        entry_date_str = request.form.get('entry_date', '').strip()

        errors: list[str] = []
        if not brand:
            errors.append('La marca es obligatoria.')
        if not model_name:
            errors.append('El modelo es obligatorio.')
        if not year or not year.isdigit():
            errors.append('El año debe ser numérico.')
        if not vin:
            errors.append('El VIN es obligatorio.')
        if not color:
            errors.append('El color es obligatorio.')
        if not price:
            errors.append('El precio es obligatorio.')

        entry_date = None
        if entry_date_str:
            try:
                entry_date = datetime.strptime(entry_date_str, '%Y-%m-%d').date()
            except ValueError:
                errors.append('La fecha de ingreso debe tener formato YYYY-MM-DD.')
        else:
            entry_date = car.entry_date

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('form.html', car=car, form=request.form)

        try:
            year_int = int(year)
            price_float = float(price)
        except ValueError:
            flash('Año y precio deben ser numéricos.', 'danger')
            return render_template('form.html', car=car, form=request.form)

        # Ensure VIN uniqueness if changed
        existing = Car.query.filter_by(vin=vin).first()
        if existing and existing.id != car.id:
            flash('Ya existe un vehículo con ese VIN.', 'danger')
            return render_template('form.html', car=car, form=request.form)

        # Update fields
        car.brand = brand
        car.model = model_name
        car.year = year_int
        car.vin = vin
        car.color = color
        car.price = price_float
        car.status = status
        car.entry_date = entry_date
        db.session.commit()
        flash('Vehículo actualizado con éxito.', 'success')
        return redirect(url_for('main.list_cars'))
    # GET: show form with existing values
    return render_template('form.html', car=car, form=car.to_dict())


@bp.route('/cars/<int:car_id>/delete', methods=['POST'])
def delete_car(car_id: int):
    """Delete a car from inventory."""
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    flash('Vehículo eliminado con éxito.', 'success')
    return redirect(url_for('main.list_cars'))


# JSON endpoints for API clients

@bp.route('/api/cars', methods=['POST'])
def api_create_car():
    """API endpoint to create a car via JSON.

    Accepts a JSON payload with the required fields.  Returns the
    created car as JSON or an error message with status 400.
    """
    data = request.get_json() or {}
    required_fields = ['brand', 'model', 'year', 'vin', 'color', 'price']
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return {"error": f"Campos faltantes: {', '.join(missing)}"}, 400
    try:
        car = Car(
            brand=data['brand'],
            model=data['model'],
            year=int(data['year']),
            vin=data['vin'],
            color=data['color'],
            price=float(data['price']),
            status=data.get('status', 'Disponible'),
            entry_date=datetime.strptime(data.get('entry_date', datetime.today().date().isoformat()), '%Y-%m-%d').date(),
        )
    except Exception as e:
        return {"error": str(e)}, 400
    # Ensure uniqueness of VIN
    if Car.query.filter_by(vin=car.vin).first():
        return {"error": "VIN duplicado"}, 400
    db.session.add(car)
    db.session.commit()
    return car.to_dict(), 201


@bp.route('/api/cars/<int:car_id>', methods=['GET'])
def api_get_car(car_id: int):
    car = Car.query.get_or_404(car_id)
    return car.to_dict()


@bp.route('/api/cars/<int:car_id>', methods=['PUT'])
def api_update_car(car_id: int):
    car = Car.query.get_or_404(car_id)
    data = request.get_json() or {}
    # Update allowed fields
    for field in ['brand', 'model', 'year', 'vin', 'color', 'price', 'status', 'entry_date']:
        if field in data:
            if field == 'year':
                setattr(car, field, int(data[field]))
            elif field == 'price':
                setattr(car, field, float(data[field]))
            elif field == 'entry_date':
                setattr(car, field, datetime.strptime(data[field], '%Y-%m-%d').date())
            else:
                setattr(car, field, data[field])
    # Ensure VIN uniqueness if changed
    existing = Car.query.filter_by(vin=car.vin).first()
    if existing and existing.id != car.id:
        return {"error": "VIN duplicado"}, 400
    db.session.commit()
    return car.to_dict()


@bp.route('/api/cars/<int:car_id>', methods=['DELETE'])
def api_delete_car(car_id: int):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return {"message": "Vehículo eliminado"}, 200