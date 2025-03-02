

from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from exts import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from datetime import date, datetime
from models import calculate_depreciation_end_date  # Ensure to import the function

# Define the Namespace for 'assets' API operations
asset_ns = Namespace('assets', description='Asset operations')

# Define the Asset Model for serialization
Asset_model = asset_ns.model(
    'Asset',
    {
        'item': fields.String(required=True, description='Item name'),
        'id': fields.Integer(description='Asset ID'),
        'specifications': fields.String(required=True, description='Specifications'),
        'class_code': fields.String(required=True, description='Class code'),
        'serial_no': fields.String(required=True, description='Serial number'),
        'purchase_date': fields.String(description='Purchase date (YYYY-MM-DD, optional, defaults to today)'),
        'depreciation_rate': fields.Float(required=True, description='Depreciation rate'),
        'vendor': fields.String(required=True, description='Vendor'),
        'purchase_price': fields.Float(required=True, description='Purchase price'),
        'condition': fields.String(required=True, description='Condition'),
        'location_name': fields.String(description='Location Name of the asset'),
        'depreciation_end_date': fields.String(description='Depreciation End Date'),
        'assignment_id': fields.Integer(description='Assignment ID'),
        'assigned_to': fields.String(description='Assigned To'),
        'status': fields.String(description='Asset status', default='unassigned')
    }
)

@asset_ns.route('/')
class AssetList(Resource):
    def get(self):
        """Get a list of all assets."""
        query = text("""
            SELECT a.id, a.item, a.specifications, a.class_code, a.serial_no, 
                   COALESCE(a.purchase_date, '1970-01-01') AS purchase_date,  
                   a.depreciation_rate, a.vendor, a.purchase_price, a.condition, a.status,
                   COALESCE(l.id::TEXT, 'N/A') AS location_id, 
                   COALESCE(l.name, 'N/A') AS location_name, 
                   ass.id AS assignment_id, ass.assigned_to
            FROM asset a
            LEFT JOIN location l ON a.location_id = l.id
            LEFT JOIN assignment ass ON a.id = ass.asset_id
        """)
        
        with db.engine.connect() as connection:
            result = connection.execute(query)
            assets = []
            for row in result.mappings():
                asset = {key: (value.isoformat() if isinstance(value, date) else value) for key, value in row.items()}
                purchase_date = asset.get('purchase_date')
                if purchase_date and purchase_date != '1970-01-01':
                    purchase_date = date.fromisoformat(purchase_date)
                    asset['depreciation_end_date'] = calculate_depreciation_end_date(
                        asset['purchase_price'], asset['depreciation_rate'], purchase_date
                    ).isoformat()
                else:
                    asset['depreciation_end_date'] = None
                
                assets.append(asset)
        
        return assets, 200
    
    @asset_ns.expect(Asset_model)
    def post(self):
        """Create a new asset."""
        data = request.get_json()
        data['purchase_date'] = data.get('purchase_date', date.today().isoformat())
        data['status'] = data.get('status', 'unassigned')

        query = text("""
            INSERT INTO asset (item, specifications, class_code, serial_no, purchase_date, 
                              depreciation_rate, vendor, purchase_price, condition, status)
            VALUES (:item, :specifications, :class_code, :serial_no, :purchase_date,  
                    :depreciation_rate, :vendor, :purchase_price, :condition, :status)
            RETURNING id
        """)

        try:
            with db.engine.connect() as connection:
                result = connection.execute(query, data)
                connection.commit()
                asset_id = result.scalar()
            return {'message': 'Asset added successfully', 'id': asset_id}, 201
        except IntegrityError as e:
            return {'message': f'Integrity error: {str(e.orig)}'}, 400
        except Exception as e:
            return {'message': f'Error adding asset: {str(e)}'}, 500

@asset_ns.route('/filter')
class AssetFilter(Resource):
    def get(self):
        """Filter assets based on query parameters."""
        params = request.args.to_dict()
        query = text("SELECT * FROM asset WHERE " + " AND ".join(f"{key} = :{key}" for key in params))

        with db.engine.connect() as connection:
            result = connection.execute(query, params).mappings().all()
            assets = []
            
            for row in result:
                asset = dict(row)
                
                # Convert purchase_date to ISO format safely
                purchase_date = asset.get('purchase_date')
                if purchase_date:
                    if isinstance(purchase_date, str):  # If it's a string, convert it to a date
                        purchase_date = date.fromisoformat(purchase_date)
                    elif isinstance(purchase_date, datetime):  # If it's a datetime object, extract date
                        purchase_date = purchase_date.date()
                    
                    depreciation_end_date = calculate_depreciation_end_date(
                        asset['purchase_price'], asset['depreciation_rate'], purchase_date
                    ).isoformat()
                else:  
                    depreciation_end_date = None  
                    
                asset['depreciation_end_date'] = depreciation_end_date    
                asset['purchase_date'] = purchase_date.isoformat() if purchase_date else None  # Ensure ISO format
                
                assets.append(asset)

        return assets, 200


@asset_ns.route('/<int:id>')
class AssetResource(Resource):
    def get(self, id):
        """Get asset by ID."""
        query = text("""
            SELECT a.id, a.item, a.specifications, a.class_code, a.serial_no, 
                   COALESCE(a.purchase_date, '1970-01-01') AS purchase_date,  
                   a.depreciation_rate, a.vendor, a.purchase_price, a.condition, a.status,
                   COALESCE(l.id::TEXT, 'N/A') AS location_id, 
                   COALESCE(l.name, 'N/A') AS location_name, 
                   ass.id AS assignment_id, ass.assigned_to
            FROM asset a
            LEFT JOIN location l ON a.location_id = l.id
            LEFT JOIN assignment ass ON a.id = ass.asset_id
            WHERE a.id = :id
        """)

        with db.engine.connect() as connection:
            result = connection.execute(query, {'id': id}).mappings().first()

        if not result:
            return {'message': 'Asset not found'}, 404

        asset = {key: (value.isoformat() if isinstance(value, date) else value) for key, value in result.items()}
        purchase_date = asset.get('purchase_date')
        if purchase_date and purchase_date != '1970-01-01':
            purchase_date = date.fromisoformat(purchase_date)
            asset['depreciation_end_date'] = calculate_depreciation_end_date(
                asset['purchase_price'], asset['depreciation_rate'], purchase_date
            ).isoformat()
        else:
            asset['depreciation_end_date'] = None

        return asset, 200


    @asset_ns.expect(Asset_model)
    def put(self, id):
        """Update asset by ID."""
        data = request.get_json()

        if not data:
            return {'message': 'No data provided for update'}, 400

        update_fields = []
        params = {'id': id}

        # Prepare dynamic update fields
        for key, value in data.items():
            if value is not None:
                update_fields.append(f"{key} = :{key}")
                params[key] = value

        if not update_fields:
            return {'message': 'No valid fields provided for update'}, 400

        # If depreciation_rate or purchase_price is updated, recalculate depreciation_end_date
        if 'depreciation_rate' in data or 'purchase_price' in data:
            query = text("SELECT purchase_price, depreciation_rate, purchase_date FROM asset WHERE id = :id")
            with db.engine.connect() as connection:
                existing_asset = connection.execute(query, {'id': id}).fetchone()

            if existing_asset:
                purchase_price = data.get('purchase_price', existing_asset.purchase_price)
                depreciation_rate = data.get('depreciation_rate', existing_asset.depreciation_rate)
                purchase_date = existing_asset.purchase_date
                depreciation_end_date = calculate_depreciation_end_date(purchase_price, depreciation_rate, purchase_date)

                # Ensure depreciation_end_date is not added twice
                if "depreciation_end_date = :depreciation_end_date" not in update_fields:
                    update_fields.append("depreciation_end_date = :depreciation_end_date")
                    params['depreciation_end_date'] = depreciation_end_date

        # Construct dynamic update query
        update_query = text(f"UPDATE asset SET {', '.join(update_fields)} WHERE id = :id")

        with db.engine.connect() as connection:
            connection.execute(update_query, params)
            connection.commit()

        return {'message': 'Asset updated successfully'}, 200

    def delete(self, id):
        """Delete asset by ID."""
        delete_query = text("DELETE FROM asset WHERE id = :id")
        with db.engine.connect() as connection:
            connection.execute(delete_query, {'id': id})
            connection.commit()
        
        return {'message': 'Asset deleted successfully'}, 200

@asset_ns.route('/return/<int:id>')
class AssetReturn(Resource):
    def post(self, id):
        """Return an asset and mark it as unassigned."""
        update_query = text("""
            UPDATE asset 
            SET status = 'unassigned', assignment_id = NULL, assigned_to = NULL
            WHERE id = :id
        """)

        try:
            with db.engine.connect() as connection:
                result = connection.execute(update_query, {'id': id})
                connection.commit()

            if result.rowcount == 0:
                return {'message': 'Asset not found or already unassigned'}, 404

            return {'message': 'Asset returned successfully and marked as unassigned'}, 200

        except Exception as e:
            return {'message': f'Error returning asset: {str(e)}'}, 500

# Function to register routes
def register_routes(api):
    api.add_namespace(asset_ns)