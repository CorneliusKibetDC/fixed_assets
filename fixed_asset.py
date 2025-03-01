

# from flask import request, jsonify
# from flask_restx import Namespace, Resource, fields
# from exts import db
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy import text
# from datetime import date
# from models import calculate_depreciation_end_date  # Ensure to import the function

# # Define the Namespace for 'assets' API operations
# asset_ns = Namespace('assets', description='Asset operations')

# # Define the Asset Model for serialization
# Asset_model = asset_ns.model(
#     'Asset',
#     {
#         'item': fields.String(required=True, description='Item name'),
#         'id': fields.Integer(description='Asset ID'),
#         'specifications': fields.String(required=True, description='Specifications'),
#         'class_code': fields.String(required=True, description='Class code'),
#         'serial_no': fields.String(required=True, description='Serial number'),
#         'purchase_date': fields.String(description='Purchase date (YYYY-MM-DD, optional, defaults to today)'),
#         'depreciation_rate': fields.Float(required=True, description='Depreciation rate'),
#         'vendor': fields.String(required=True, description='Vendor'),
#         'purchase_price': fields.Float(required=True, description='Purchase price'),
#         'condition': fields.String(required=True, description='Condition'),
#         'location_name': fields.String(description='Location Name of the asset'),
#         'depreciation_end_date': fields.String(description='Depreciation End Date'),
#         'assignment_id': fields.Integer(description='Assignment ID'),
#         'assigned_to': fields.String(description='Assigned To')
#     }
# )

# @asset_ns.route('/')
# class AssetList(Resource):
#     def get(self):
#         """Get a list of all assets, including their locations and assignments."""
#         query = text("""
#             SELECT a.id, a.item, a.specifications, a.class_code, a.serial_no, a.purchase_date, 
#                    a.depreciation_rate, a.vendor, a.purchase_price, a.condition, 
#                    COALESCE(l.id::TEXT, 'N/A') AS location_id, 
#                    COALESCE(l.name, 'N/A') AS location_name, 
#                    ass.id AS assignment_id, ass.assigned_to
#             FROM asset a
#             LEFT JOIN location l ON a.location_id = l.id
#             LEFT JOIN assignment ass ON a.id = ass.asset_id
#         """)

#         # Optional filtering
#         filter_item = request.args.get('item', None)
#         filter_class_code = request.args.get('class_code', None)

#         conditions = []
#         params = {}

#         if filter_item:
#             conditions.append("a.item ILIKE :item")
#             params['item'] = f'%{filter_item}%'
        
#         if filter_class_code:
#             conditions.append("a.class_code ILIKE :class_code")
#             params['class_code'] = f'%{filter_class_code}%'

#         if conditions:
#             query = text(f"{query} WHERE {' AND '.join(conditions)}")

#         with db.engine.connect() as connection:
#             result = connection.execute(query, params) if params else connection.execute(query)
#             assets = []
#             for row in result.mappings():
#                 asset = {key: (value.isoformat() if isinstance(value, date) else value) for key, value in row.items()}
#                 asset.pop('depreciation_start_date', None)  # Remove depreciation start date if present
                
#                 purchase_date = asset.get('purchase_date')
#                 purchase_price = asset.get('purchase_price')
#                 depreciation_rate = asset.get('depreciation_rate')
                
#                 if not asset.get('depreciation_end_date') and purchase_date and purchase_price is not None and depreciation_rate is not None:
#                     try:
#                         asset['depreciation_end_date'] = calculate_depreciation_end_date(
#                             purchase_price,
#                             depreciation_rate,
#                             date.fromisoformat(purchase_date)
#                         ).isoformat()
#                     except Exception as e:
#                         asset['depreciation_end_date'] = None
                
#                 assets.append(asset)
#         return assets, 200

#     @asset_ns.expect(Asset_model)
#     def post(self):
#         """Create a new asset"""
#         data = request.get_json()
#         purchase_date = data.get('purchase_date') or date.today().isoformat()
#         data['purchase_date'] = purchase_date

#         query = text("""
#             INSERT INTO asset (item, specifications, class_code, serial_no, purchase_date, 
#                               depreciation_rate, vendor, purchase_price, condition)
#             VALUES (:item, :specifications, :class_code, :serial_no, :purchase_date,  
#                     :depreciation_rate, :vendor, :purchase_price, :condition)
#             RETURNING id
#         """)

#         try:
#             with db.engine.connect() as connection:
#                 result = connection.execute(query, data)
#                 connection.commit()
#                 asset_id = result.scalar()
#             return {'message': 'Asset added successfully', 'id': asset_id}, 201
#         except IntegrityError as e:
#             return {'message': f'Integrity error: {str(e.orig)}'}, 400
#         except Exception as e:
#             return {'message': f'Error adding asset: {str(e)}'}, 500

# @asset_ns.route('/<int:asset_id>')
# class AssetDetail(Resource):
#     def get(self, asset_id):
#         """Get a single asset by ID, including location and assignment details."""
#         query = text("""
#             SELECT a.id, a.item, a.specifications, a.class_code, a.serial_no, a.purchase_date, 
#                    a.depreciation_rate, a.vendor, a.purchase_price, a.condition, 
#                    l.id AS location_id, l.name AS location_name, 
#                    ass.id AS assignment_id, ass.assigned_to
#             FROM asset a
#             LEFT JOIN location l ON a.location_id = l.id  
#             LEFT JOIN assignment ass ON a.id = ass.asset_id
#             WHERE a.id = :id
#         """)

#         with db.engine.connect() as connection:
#             result = connection.execute(query, {'id': asset_id}).mappings().first()
#             if not result:
#                 return {'message': 'Asset not found'}, 404
        
#         asset = {key: (value.isoformat() if isinstance(value, date) else value) for key, value in result.items()}
#         asset.pop('depreciation_start_date', None)  # Remove depreciation start date if present
        
#         purchase_date = asset.get('purchase_date')
#         purchase_price = asset.get('purchase_price')
#         depreciation_rate = asset.get('depreciation_rate')
        
#         if not asset.get('depreciation_end_date') and purchase_date and purchase_price is not None and depreciation_rate is not None:
#             try:
#                 asset['depreciation_end_date'] = calculate_depreciation_end_date(
#                     purchase_price,
#                     depreciation_rate,
#                     date.fromisoformat(purchase_date)
#                 ).isoformat()
#             except Exception as e:
#                 asset['depreciation_end_date'] = None
        
#         return jsonify(asset)

#     @asset_ns.expect(Asset_model)
#     def put(self, asset_id):
#         """Update an existing asset"""
#         data = request.get_json()
#         query = text("""
#             UPDATE asset
#             SET item = :item, specifications = :specifications, class_code = :class_code, 
#                 serial_no = :serial_no, purchase_date = :purchase_date, 
#                 depreciation_rate = :depreciation_rate, vendor = :vendor, 
#                 purchase_price = :purchase_price, condition = :condition
#             WHERE id = :id
#         """)

#         data['id'] = asset_id  # Include asset_id in the update values

#         try:
#             with db.engine.connect() as connection:
#                 result = connection.execute(query, data)
#                 connection.commit()
#                 if result.rowcount == 0:
#                     return {'message': 'Asset not found'}, 404
#             return {'message': 'Asset updated successfully'}, 200
#         except IntegrityError as e:
#             return {'message': f'Integrity error: {str(e.orig)}'}, 400
#         except Exception as e:
#             return {'message': f'Error updating asset: {str(e)}'}, 500

#     def delete(self, asset_id):
#         """Delete an asset by ID"""
#         query = text("DELETE FROM asset WHERE id = :id")

#         try:
#             with db.engine.connect() as connection:
#                 result = connection.execute(query, {'id': asset_id})
#                 connection.commit()
#                 if result.rowcount == 0:
#                     return {'message': 'Asset not found'}, 404
#             return {'message': 'Asset deleted successfully'}, 200
#         except Exception as e:
#             return {'message': f'Error deleting asset: {str(e)}'}, 500


# def register_routes(api):
#     """Register asset namespace routes"""
#     api.add_namespace(asset_ns)



# @asset_ns.route('/filter')
# class AssetFilter(Resource):
#     def get(self):
#         """Filter assets based on query parameters."""
#         params = request.args.to_dict()
#         query = text("SELECT * FROM asset WHERE " + " AND ".join(f"{key} = :{key}" for key in params))
#         with db.engine.connect() as connection:
#             result = connection.execute(query, params).mappings().all()
#             assets = [dict(row) for row in result]
#             for asset in assets:
#                 if isinstance(asset.get('purchase_date'), date):
#                     asset['purchase_date'] = asset['purchase_date'].isoformat()
#         return assets, 200










from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from exts import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from datetime import date
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
        'status': fields.String(description='Asset status', default='active')
    }
)

@asset_ns.route('/')
class AssetList(Resource):
    def get(self):
        """Get a list of all assets."""
        query = text("""
            SELECT a.id, a.item, a.specifications, a.class_code, a.serial_no, a.purchase_date, 
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
            assets = [{key: (value.isoformat() if isinstance(value, date) else value) for key, value in row.items()} for row in result.mappings()]
        
        return assets, 200
    
    @asset_ns.expect(Asset_model)
    def post(self):
        """Create a new asset."""
        data = request.get_json()
        data['purchase_date'] = data.get('purchase_date', date.today().isoformat())
        data['status'] = data.get('status', 'active')

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
                if isinstance(asset.get('purchase_date'), date):
                    asset['purchase_date'] = asset['purchase_date'].isoformat()
                assets.append(asset)

        return assets, 200

@asset_ns.route('/<int:id>')
class AssetResource(Resource):
    def get(self, id):
        """Get asset by ID."""
        query = text("""
            SELECT * FROM asset WHERE id = :id
        """)
        
        with db.engine.connect() as connection:
            result = connection.execute(query, {'id': id}).mappings().first()
        
        if not result:
            return {'message': 'Asset not found'}, 404
        
        asset = dict(result)

        # Convert date fields to strings
        for key, value in asset.items():
            if isinstance(value, date):
                asset[key] = value.isoformat()

        return asset, 200

    
    @asset_ns.expect(Asset_model)
    def put(self, id):
        """Update asset by ID."""
        data = request.get_json()
        data['id'] = id
        update_query = text("""
            UPDATE asset SET 
                item = :item, specifications = :specifications, class_code = :class_code, 
                serial_no = :serial_no, purchase_date = :purchase_date, depreciation_rate = :depreciation_rate, 
                vendor = :vendor, purchase_price = :purchase_price, condition = :condition, status = :status
            WHERE id = :id
        """)

        with db.engine.connect() as connection:
            connection.execute(update_query, data)
            connection.commit()
        
        return {'message': 'Asset updated successfully'}, 200

    def delete(self, id):
        """Delete asset by ID."""
        delete_query = text("DELETE FROM asset WHERE id = :id")
        with db.engine.connect() as connection:
            connection.execute(delete_query, {'id': id})
            connection.commit()
        
        return {'message': 'Asset deleted successfully'}, 200

# Function to register routes
def register_routes(api):
    api.add_namespace(asset_ns)


