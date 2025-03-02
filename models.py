

from exts import db
from sqlalchemy.sql import text
from datetime import date, timedelta

class Asset:
    """
    Wrapper class for interacting with the 'asset' table using raw SQL.
    """
    @staticmethod
    def add_asset(item, specifications, class_code, serial_no, location_id, depreciation_rate, purchase_price, purchase_date, vendor, condition):
        depreciation_end_date = calculate_depreciation_end_date(purchase_price, depreciation_rate, purchase_date)
        query = text("""
            INSERT INTO asset (item, specifications, class_code, serial_no, location_id, depreciation_rate, purchase_price, depreciation_end_date, purchase_date, vendor, condition)
            VALUES (:item, :specifications, :class_code, :serial_no, :location_id, :depreciation_rate, :purchase_price, :depreciation_end_date, :purchase_date, :vendor, :condition)
            RETURNING id;
        """)
        with db.engine.begin() as connection:
            result = connection.execute(query, {
                "item": item, "specifications": specifications, "class_code": class_code, "serial_no": serial_no,
                "location_id": location_id, "depreciation_rate": depreciation_rate, "purchase_price": purchase_price,
                "depreciation_end_date": depreciation_end_date, "purchase_date": purchase_date, "vendor": vendor, "condition": condition
            })
            return result.fetchone()[0]

    @staticmethod
    def get_all_assets():
        query = text("SELECT * FROM asset;")
        with db.engine.begin() as connection:
            return connection.execute(query).fetchall()

    @staticmethod
    def get_asset_by_id(asset_id):
        query = text("SELECT * FROM asset WHERE id = :id;")
        with db.engine.begin() as connection:
            return connection.execute(query, {"id": asset_id}).fetchone()

    @staticmethod
    def update_asset(asset_id, **kwargs):
        update_fields = ", ".join([f"{key} = :{key}" for key in kwargs])
        query = text(f"""
            UPDATE asset SET {update_fields} WHERE id = :id;
        """)
        with db.engine.begin() as connection:
            connection.execute(query, {**kwargs, "id": asset_id})

    @staticmethod
    def delete_asset(asset_id):
        query = text("DELETE FROM asset WHERE id = :id;")
        with db.engine.begin() as connection:
            connection.execute(query, {"id": asset_id})


def calculate_depreciation_end_date(purchase_price, depreciation_rate, purchase_date):
    if not purchase_price or not depreciation_rate or depreciation_rate <= 0:
        return None
    years_to_depreciate = 1 / (depreciation_rate / 100)
    return purchase_date + timedelta(days=int(years_to_depreciate * 365))

def create_tables():
    with db.engine.begin() as connection:
        print("\U0001F680 Ensuring tables exist...")
        connection.execute(text("""
        CREATE TABLE IF NOT EXISTS location (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(500)
        );
        """))
        connection.execute(text("""
        CREATE TABLE IF NOT EXISTS asset (
            id SERIAL PRIMARY KEY,
            item VARCHAR(255) NOT NULL,
            specifications VARCHAR(500),
            class_code VARCHAR(50),
            serial_no VARCHAR(50) UNIQUE,
            location_id INTEGER REFERENCES location(id) ON DELETE SET NULL,
            depreciation_rate FLOAT NOT NULL,
            purchase_price FLOAT NOT NULL,
            depreciation_end_date DATE,
            purchase_date DATE DEFAULT CURRENT_DATE,
            vendor VARCHAR(255),
            condition VARCHAR(50)
        );
        """))
        connection.execute(text("ALTER TABLE asset ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'unassigned';"))
        connection.execute(text("""
        CREATE TABLE IF NOT EXISTS assignment (
            id SERIAL PRIMARY KEY,
            asset_id INTEGER REFERENCES asset(id) ON DELETE CASCADE,
            location_id INTEGER REFERENCES location(id) ON DELETE CASCADE,
            assigned_to VARCHAR(255) NOT NULL,
            assigned_date DATE DEFAULT CURRENT_DATE,
            return_date DATE
        );
        """))
        print("✅ Tables checked/updated successfully.")














