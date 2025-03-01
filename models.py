
# from exts import db
# from sqlalchemy.sql import text
# from datetime import date, timedelta

# def calculate_depreciation_end_date(purchase_price, depreciation_rate, purchase_date):
#     """
#     Calculate the date when an asset will be fully depreciated.
#     Formula: Depreciation Duration (Years) = 1 / (Depreciation Rate / 100)
#     """
#     if not purchase_price or not depreciation_rate or depreciation_rate <= 0:
#         return None

#     years_to_depreciate = 1 / (depreciation_rate / 100)  # Convert rate to fraction
#     depreciation_end = purchase_date + timedelta(days=int(years_to_depreciate * 365))
    
#     return depreciation_end

# def create_tables():
#     """Ensures tables exist without dropping them."""
#     with db.engine.begin() as connection:
#         print("\U0001F680 Ensuring tables exist...")

#         # Location table to store asset locations
#         connection.execute(text("""
#         CREATE TABLE IF NOT EXISTS location (
#             id SERIAL PRIMARY KEY,
#             name VARCHAR(255) NOT NULL,
#             description VARCHAR(500)
#         );
#         """))

#         # Asset table with direct location reference
#         connection.execute(text("""
#         CREATE TABLE IF NOT EXISTS asset (
#             id SERIAL PRIMARY KEY,
#             item VARCHAR(255) NOT NULL,
#             specifications VARCHAR(500),
#             class_code VARCHAR(50),
#             serial_no VARCHAR(50) UNIQUE,
#             location_id INTEGER REFERENCES location(id) ON DELETE SET NULL,
#             depreciation_rate FLOAT NOT NULL,
#             purchase_price FLOAT NOT NULL,
#             depreciation_end_date DATE,
#             purchase_date DATE DEFAULT CURRENT_DATE,
#             vendor VARCHAR(255),
#             condition VARCHAR(50)
#         );
#         """))

#         # Assignment table tracks asset assignments
#         connection.execute(text("""
#         CREATE TABLE IF NOT EXISTS assignment (
#             id SERIAL PRIMARY KEY,
#             asset_id INTEGER REFERENCES asset(id) ON DELETE CASCADE,
#             location_id INTEGER REFERENCES location(id) ON DELETE CASCADE,
#             assigned_to VARCHAR(255) NOT NULL,
#             assigned_date DATE DEFAULT CURRENT_DATE,
#             return_date DATE
#         );
#         """))

#         print("✅ Tables checked/created successfully.")

# # def get_asset_with_assignments(asset_id):
# #     """Retrieve asset details including location and assignment details."""
# #     with db.engine.begin() as connection:
# #         result = connection.execute(text("""
# #         SELECT a.id, a.item, a.class_code, a.serial_no, a.purchase_date, 
# #                a.depreciation_rate, a.depreciation_end_date, a.vendor, 
# #                a.location_id, l.name AS location_name,
# #                ass.id AS assignment_id, ass.assigned_to
# #         FROM asset a
# #         LEFT JOIN location l ON a.location_id = l.id
# #         LEFT JOIN assignment ass ON a.id = ass.asset_id
# #         WHERE a.id = :id;
# #         """), {"id": asset_id})

# #         asset = result.fetchone()
# #         if asset:
# #             return dict(asset)
# #         return None

# # def assign_asset(asset_id, location_id, assigned_to):
# #     """Assign an asset to a location and update its location_id."""
# #     with db.engine.begin() as connection:
# #         # Create assignment
# #         connection.execute(text("""
# #         INSERT INTO assignment (asset_id, location_id, assigned_to)
# #         VALUES (:asset_id, :location_id, :assigned_to);
# #         """), {"asset_id": asset_id, "location_id": location_id, "assigned_to": assigned_to})

# #         # Update asset.location_id so it's always set
# #         connection.execute(text("""
# #         UPDATE asset 
# #         SET location_id = :location_id 
# #         WHERE id = :asset_id;
# #         """), {"location_id": location_id, "asset_id": asset_id})

# #         print(f"✅ Asset {asset_id} assigned to location {location_id} and updated.")









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














