from datetime import date

def cargar_demo_si_vacio(db):
    # Import diferido (para evitar ciclos de importación con models)
    from autogo_erp.models import Vehicle, AcquisitionType

    # Si ya hay vehículos, no hace nada
    if db.query(Vehicle).count() > 0:
        return

    demo_items = [
        Vehicle(
            vin="DEMO1234567890001",
            brand="Toyota",
            model="Corolla",
            year=2018,
            odometer_km=65432,
            acquisition_type=AcquisitionType.DIRECT_SALE,
            seller_name="Demo Seller 1",
            seller_contact="+50760000001",
            seller_document="CED-8-111-111",
            received_date=date(2025, 8, 1),
        ),
        Vehicle(
            vin="DEMO1234567890002",
            brand="Hyundai",
            model="Elantra",
            year=2019,
            odometer_km=40210,
            acquisition_type=AcquisitionType.TRADE_IN,
            seller_name="Demo Seller 2",
            seller_contact="+50760000002",
            seller_document="CED-8-222-222",
            received_date=date(2025, 8, 5),
        ),
    ]

    db.add_all(demo_items)
    db.commit()

