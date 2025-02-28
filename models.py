# from exts import db
# from sqlalchemy.sql import text
# from datetime import date, timedelta

# def calculate_depreciation_end_date(purchase_price, depreciation_rate, purchase_date):
#     """
#     Calculate the date when an asset will be fully depreciated.
#     """
#     if not purchase_price or not depreciation_rate or depreciation_rate <= 0:
#         return None

#     years_to_depreciate = 1 / (depreciation_rate / 100)
#     depreciation_end = purchase_date + timedelta(days=int(years_to_depreciate * 365))
    
#     return depreciation_end

# def create_tables():
#     """Ensures tables exist without dropping them."""
#     with db.engine.begin() as connection:
#         print("🚀 Ensuring tables exist...")

#         connection.execute(text("""
#         CREATE TABLE IF NOT EXISTS location (
#             id SERIAL PRIMARY KEY,
#             name VARCHAR(255) NOT NULL,
#             description VARCHAR(500)
#         );
#         """))

#         connection.execute(text("""
#         CREATE TABLE IF NOT EXISTS assignment (
#             id SERIAL PRIMARY KEY,
#             asset_id INTEGER,
#             location_id INTEGER REFERENCES location(id) ON DELETE CASCADE,
#             assigned_to VARCHAR(255) NOT NULL,
#             assigned_date DATE DEFAULT CURRENT_DATE,
#             return_date DATE
#         );
#         """))

#         connection.execute(text("""
#         CREATE TABLE IF NOT EXISTS asset (
#             id SERIAL PRIMARY KEY,  -- ✅ Auto-incremented ID
#             item VARCHAR(255) NOT NULL,
#             specifications VARCHAR(500),
#             class_code VARCHAR(50),
#             serial_no VARCHAR(50) UNIQUE,
#             assignment_id INTEGER REFERENCES assignment(id) ON DELETE CASCADE,
#             depreciation_rate FLOAT NOT NULL,
#             purchase_price FLOAT NOT NULL,
#             depreciation_end_date DATE,
#             purchase_date DATE DEFAULT CURRENT_DATE,
#             location_id INTEGER REFERENCES location(id) ON DELETE CASCADE,
#             vendor VARCHAR(255),
#             condition VARCHAR(50)
#         );
#         """))

#         print("✅ Tables checked/created successfully.")




# from exts import db
# from sqlalchemy.sql import text
# from datetime import date, timedelta

# def calculate_depreciation_end_date(purchase_price, depreciation_rate, purchase_date):
#     """
#     Calculate the date when an asset will be fully depreciated.
#     Formula: Depreciation Duration (Years) = Purchase Price / (Depreciation Rate * Purchase Price)
#     """
#     if not purchase_price or not depreciation_rate or depreciation_rate <= 0:
#         return None

#     years_to_depreciate = 1 / (depreciation_rate / 100)  # Convert rate to fraction
#     depreciation_end = purchase_date + timedelta(days=int(years_to_depreciate * 365))

#     return depreciation_end

# def create_tables():
#     """Ensures tables exist without dropping them."""
#     with db.engine.begin() as connection:
#         print("🚀 Ensuring tables exist...")

#         connection.execute(text("""
#         CREATE TABLE IF NOT EXISTS location (
#             id SERIAL PRIMARY KEY,
#             name VARCHAR(255) NOT NULL,
#             description VARCHAR(500)
#         );
#         """))

#         connection.execute(text("""
#         CREATE TABLE IF NOT EXISTS assignment (
#             id SERIAL PRIMARY KEY,
#             asset_id INTEGER,
#             location_id INTEGER REFERENCES location(id) ON DELETE CASCADE,
#             assigned_to VARCHAR(255) NOT NULL,
#             assigned_date DATE DEFAULT CURRENT_DATE,
#             return_date DATE
#         );
#         """))

#         connection.execute(text("""
#         CREATE TABLE IF NOT EXISTS asset (
#             id SERIAL PRIMARY KEY,
#             item VARCHAR(255) NOT NULL,
#             specifications VARCHAR(500),
#             class_code VARCHAR(50),
#             serial_no VARCHAR(50) UNIQUE,
#             assignment_id INTEGER REFERENCES assignment(id) ON DELETE CASCADE,
#             depreciation_rate FLOAT NOT NULL,
#             purchase_price FLOAT NOT NULL,
#             depreciation_start_date DATE DEFAULT CURRENT_DATE,
#             depreciation_end_date DATE,
#             purchase_date DATE DEFAULT CURRENT_DATE,
#             location_id INTEGER REFERENCES location(id) ON DELETE CASCADE,
#             vendor VARCHAR(255),
#             condition VARCHAR(50)
#         );
#         """))

#         print("✅ Tables checked/created successfully.")








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
#         print("🚀 Ensuring tables exist...")

#         connection.execute(text("""
#         CREATE TABLE IF NOT EXISTS location (
#             id SERIAL PRIMARY KEY,
#             name VARCHAR(255) NOT NULL,
#             description VARCHAR(500)
#         );
#         """))

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

#         connection.execute(text("""
#         CREATE TABLE IF NOT EXISTS asset (
#             id SERIAL PRIMARY KEY,
#             item VARCHAR(255) NOT NULL,
#             specifications VARCHAR(500),
#             class_code VARCHAR(50),
#             serial_no VARCHAR(50) UNIQUE,
#             assignment_id INTEGER REFERENCES assignment(id) ON DELETE CASCADE,
#             depreciation_rate FLOAT NOT NULL,
#             purchase_price FLOAT NOT NULL,
#             depreciation_end_date DATE,
#             purchase_date DATE DEFAULT CURRENT_DATE,
#             vendor VARCHAR(255),
#             condition VARCHAR(50)
#         );
#         """))

#         print("✅ Tables checked/created successfully.")








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
#         print("🚀 Ensuring tables exist...")

#         # Location table to store asset locations
#         connection.execute(text("""
#         CREATE TABLE IF NOT EXISTS location (
#             id SERIAL PRIMARY KEY,
#             name VARCHAR(255) NOT NULL,
#             description VARCHAR(500)
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

#         # Asset table with direct location reference
#         connection.execute(text("""
#         CREATE TABLE IF NOT EXISTS asset (
#             id SERIAL PRIMARY KEY,
#             item VARCHAR(255) NOT NULL,
#             specifications VARCHAR(500),
#             class_code VARCHAR(50),
#             serial_no VARCHAR(50) UNIQUE,
#             location_id INTEGER REFERENCES location(id) ON DELETE SET NULL,  -- Direct link to location
#             depreciation_rate FLOAT NOT NULL,
#             purchase_price FLOAT NOT NULL,
#             depreciation_end_date DATE,
#             purchase_date DATE DEFAULT CURRENT_DATE,
#             vendor VARCHAR(255),
#             condition VARCHAR(50)
#         );
#         """))

#         print("✅ Tables checked/created successfully.")






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
#         print("🚀 Ensuring tables exist...")

#         # Location table to store asset locations
#         connection.execute(text("""
#         CREATE TABLE IF NOT EXISTS location (
#             id SERIAL PRIMARY KEY,
#             name VARCHAR(255) NOT NULL,
#             description VARCHAR(500)
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

#         # Asset table with direct location reference
#         connection.execute(text("""
#         CREATE TABLE IF NOT EXISTS asset (
#             id SERIAL PRIMARY KEY,
#             item VARCHAR(255) NOT NULL,
#             specifications VARCHAR(500),
#             class_code VARCHAR(50),
#             serial_no VARCHAR(50) UNIQUE,
#             location_id INTEGER REFERENCES location(id) ON DELETE SET NULL,  -- ✅ Direct link to location
#             depreciation_rate FLOAT NOT NULL,
#             purchase_price FLOAT NOT NULL,
#             depreciation_end_date DATE,
#             purchase_date DATE DEFAULT CURRENT_DATE,
#             vendor VARCHAR(255),
#             condition VARCHAR(50)
#         );
#         """))

#         print("✅ Tables checked/created successfully.")

# def get_asset_by_id(asset_id):
#     """Retrieve asset details including location name."""
#     with db.engine.begin() as connection:
#         result = connection.execute(text("""
#         SELECT a.id, a.item, a.class_code, a.serial_no, a.purchase_date, 
#                a.depreciation_rate, a.depreciation_end_date, a.vendor, 
#                ass.id AS assignment_id, ass.location_id, ass.assigned_to,
#                l.name AS location_name  -- ✅ Fetch location name
#         FROM asset a
#         LEFT JOIN assignment ass ON a.id = ass.asset_id
#         LEFT JOIN location l ON a.location_id = l.id  -- ✅ Correct join
#         WHERE a.id = :id;
#         """), {"id": asset_id})

#         asset = result.fetchone()
#         if asset:
#             return dict(asset)  # Convert row to dictionary
#         return None

# def assign_asset(asset_id, location_id, assigned_to):
#     """Assign an asset to a location and update its location_id."""
#     with db.engine.begin() as connection:
#         # Create assignment
#         connection.execute(text("""
#         INSERT INTO assignment (asset_id, location_id, assigned_to)
#         VALUES (:asset_id, :location_id, :assigned_to);
#         """), {"asset_id": asset_id, "location_id": location_id, "assigned_to": assigned_to})

#         # ✅ Update asset.location_id so it's always set
#         connection.execute(text("""
#         UPDATE asset 
#         SET location_id = :location_id 
#         WHERE id = :asset_id;
#         """), {"location_id": location_id, "asset_id": asset_id})

#         print(f"✅ Asset {asset_id} assigned to location {location_id} and updated.")







from exts import db
from sqlalchemy.sql import text
from datetime import date, timedelta

def calculate_depreciation_end_date(purchase_price, depreciation_rate, purchase_date):
    """
    Calculate the date when an asset will be fully depreciated.
    Formula: Depreciation Duration (Years) = 1 / (Depreciation Rate / 100)
    """
    if not purchase_price or not depreciation_rate or depreciation_rate <= 0:
        return None

    years_to_depreciate = 1 / (depreciation_rate / 100)  # Convert rate to fraction
    depreciation_end = purchase_date + timedelta(days=int(years_to_depreciate * 365))

    return depreciation_end

def create_tables():
    """Ensures tables exist without dropping them."""
    with db.engine.begin() as connection:
        print("\U0001F680 Ensuring tables exist...")

        # Location table to store asset locations
        connection.execute(text("""
        CREATE TABLE IF NOT EXISTS location (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(500)
        );
        """))

        # Asset table with direct location reference
        connection.execute(text("""
        CREATE TABLE IF NOT EXISTS asset (
            id SERIAL PRIMARY KEY,
            item VARCHAR(255) NOT NULL,
            specifications VARCHAR(500),
            class_code VARCHAR(50),
            serial_no VARCHAR(50) UNIQUE,
            location_id INTEGER REFERENCES location(id) ON DELETE SET NULL,  -- ✅ Direct link to location
            depreciation_rate FLOAT NOT NULL,
            purchase_price FLOAT NOT NULL,
            depreciation_end_date DATE,
            purchase_date DATE DEFAULT CURRENT_DATE,
            vendor VARCHAR(255),
            condition VARCHAR(50)
        );
        """))

        # Assignment table tracks asset assignments
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

        print("✅ Tables checked/created successfully.")

def get_asset_by_id(asset_id):
    """Retrieve asset details including location name."""
    with db.engine.begin() as connection:
        result = connection.execute(text("""
        SELECT a.id, a.item, a.class_code, a.serial_no, a.purchase_date, 
               a.depreciation_rate, a.depreciation_end_date, a.vendor, 
               a.location_id, l.name AS location_name  -- ✅ Fetch location name
        FROM asset a
        LEFT JOIN location l ON a.location_id = l.id  -- ✅ Correct join
        WHERE a.id = :id;
        """), {"id": asset_id})

        asset = result.fetchone()
        if asset:
            return dict(asset)  # Convert row to dictionary
        return None

def assign_asset(asset_id, location_id, assigned_to):
    """Assign an asset to a location and update its location_id."""
    with db.engine.begin() as connection:
        # Create assignment
        connection.execute(text("""
        INSERT INTO assignment (asset_id, location_id, assigned_to)
        VALUES (:asset_id, :location_id, :assigned_to);
        """), {"asset_id": asset_id, "location_id": location_id, "assigned_to": assigned_to})

        # ✅ Update asset.location_id so it's always set
        connection.execute(text("""
        UPDATE asset 
        SET location_id = :location_id 
        WHERE id = :asset_id;
        """), {"location_id": location_id, "asset_id": asset_id})

        print(f"✅ Asset {asset_id} assigned to location {location_id} and updated.")
