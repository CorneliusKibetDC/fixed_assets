








# from flask import request, jsonify
# from flask_restx import Namespace, Resource, fields
# from exts import db
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy import text
# from datetime import date

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
#         'location_id': fields.Integer(required=True, description='Location ID'),
#         'depreciation_rate': fields.Float(required=True, description='Depreciation rate'),
#         'vendor': fields.String(required=True, description='Vendor'),
#         'purchase_price': fields.Float(required=True, description='Purchase price'),
#         'condition': fields.String(required=True, description='Condition')
#     }
# )

# @asset_ns.route('/')
# class AssetList(Resource):
#     def get(self):
#         """
#         Get a list of all assets
#         """
#         query = text("SELECT * FROM asset")
#         with db.engine.connect() as connection:
#             result = connection.execute(query)
#             assets = [
#                 {key: (value.isoformat() if isinstance(value, date) else value) for key, value in row.items()}
#                 for row in result.mappings()
#             ]
#         return assets, 200

#     @asset_ns.expect(Asset_model)
#     def post(self):
#         """
#         Create a new asset
#         """
#         data = request.get_json()

#         purchase_date = data.get('purchase_date')  # Get purchase_date if provided
#         if not purchase_date:  
#             purchase_date = None  # Let the DB set it to CURRENT_DATE

#         query = text("""
#             INSERT INTO asset (item, specifications, class_code, serial_no, purchase_date, 
#                               depreciation_rate, vendor, purchase_price, condition)
#             VALUES (:item, :specifications, :class_code, :serial_no, :purchase_date, :location_id, 
#                     :depreciation_rate, :vendor, :purchase_price, :condition)
#             RETURNING id
#         """)

#         try:
#             with db.engine.connect() as connection:
#                 result = connection.execute(query, {
#                     'item': data['item'],
#                     'specifications': data['specifications'],
#                     'class_code': data['class_code'],
#                     'serial_no': data['serial_no'],
#                     'purchase_date': purchase_date,  # Pass None if not provided
#                     'depreciation_rate': data['depreciation_rate'],
#                     'vendor': data['vendor'],
#                     'purchase_price': data['purchase_price'],
#                     'condition': data['condition']
#                 })
#                 connection.commit()
#                 asset_id = result.scalar()
#             return {'message': 'Asset added successfully', 'id': asset_id}, 201
#         except IntegrityError as e:
#             return {'message': f'Integrity error: {str(e)}'}, 400
#         except Exception as e:
#             return {'message': f'Error adding asset: {str(e)}'}, 500

# @asset_ns.route('/<int:asset_id>')
# class AssetDetail(Resource):
#     def get(self, asset_id):
#         """
#         Get a single asset by ID
#         """
#         query = text("SELECT * FROM asset WHERE id = :id")
#         with db.engine.connect() as connection:
#             result = connection.execute(query, {'id': asset_id}).mappings().first()
#             if not result:
#                 return {'message': 'Asset not found'}, 404
        
#         asset = {key: (value.isoformat() if isinstance(value, date) else value) for key, value in result.items()}
#         return asset, 200

#     def delete(self, asset_id):
#         """
#         Delete an asset by ID
#         """
#         query = text("DELETE FROM asset WHERE id = :id")
#         with db.engine.connect() as connection:
#             result = connection.execute(query, {'id': asset_id})
#             connection.commit()
#             if result.rowcount == 0:
#                 return {'message': 'Asset not found'}, 404
#         return {'message': 'Asset deleted successfully'}, 204

#     @asset_ns.expect(Asset_model)
#     def put(self, asset_id):
#         """
#         Update an asset by ID
#         """
#         data = request.get_json()
#         update_fields = []
#         update_params = {'id': asset_id}

#         # 🔹 Build dynamic SQL query based on provided fields
#         for field, value in data.items():
#             update_fields.append(f"{field} = :{field}")
#             update_params[field] = value

#         if not update_fields:
#             return {'message': 'No fields provided for update'}, 400

#         query = text(f"""
#             UPDATE asset
#             SET {", ".join(update_fields)}
#             WHERE id = :id
#             RETURNING id
#         """)

#         with db.engine.connect() as connection:
#             result = connection.execute(query, update_params)
#             connection.commit()
#             if result.rowcount == 0:
#                 return {'message': 'Asset not found'}, 404

#         return {'message': 'Asset updated successfully'}, 200

# @asset_ns.route('/filter')
# class AssetFilter(Resource):
#     def post(self):
#         """
#         Get assets based on filters
#         """
#         filters = request.get_json()
#         query = "SELECT * FROM asset WHERE 1=1"
#         params = {}

#         if 'location_id' in filters:
#             query += " AND location_id = :location_id"
#             params['location_id'] = filters['location_id']

#         if 'class_code' in filters:
#             query += " AND class_code = :class_code"
#             params['class_code'] = filters['class_code']

#         if 'depreciation_start_date' in filters:
#             query += " AND depreciation_start_date >= :depreciation_start_date"
#             params['depreciation_start_date'] = filters['depreciation_start_date']

#         if 'depreciation_end_date' in filters:
#             query += " AND depreciation_end_date <= :depreciation_end_date"
#             params['depreciation_end_date'] = filters['depreciation_end_date']

#         with db.engine.connect() as connection:
#             result = connection.execute(text(query), params)
#             assets = [
#                 {key: (value.isoformat() if isinstance(value, date) else value) for key, value in row.items()}
#                 for row in result.mappings()
#             ]

#         if not assets:
#             return {'message': 'No assets found matching the provided filters'}, 200

#         return assets, 200

# def register_routes(api):
#     """
#     Register asset namespace routes
#     """
#     api.add_namespace(asset_ns)











# from flask import request, jsonify
# from flask_restx import Namespace, Resource, fields
# from exts import db
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy import text
# from datetime import date

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
#         'condition': fields.String(required=True, description='Condition')
#     }
# )

# @asset_ns.route('/')
# class AssetList(Resource):
#     def get(self):
#         """
#         Get a list of all assets
#         """
#         query = text("SELECT * FROM asset")
#         with db.engine.connect() as connection:
#             result = connection.execute(query)
#             assets = [
#                 {key: (value.isoformat() if isinstance(value, date) else value) for key, value in row.items()}
#                 for row in result.mappings()
#             ]
#         return assets, 200

#     @asset_ns.expect(Asset_model)
#     def post(self):
#         """
#         Create a new asset
#         """
#         data = request.get_json()

#         purchase_date = data.get('purchase_date')  # Get purchase_date if provided
#         if not purchase_date:  
#             purchase_date = None  # Let the DB set it to CURRENT_DATE

#         query = text("""
#             INSERT INTO asset (item, specifications, class_code, serial_no, purchase_date, 
#                               depreciation_rate, vendor, purchase_price, condition)
#             VALUES (:item, :specifications, :class_code, :serial_no, :purchase_date,  
#                     :depreciation_rate, :vendor, :purchase_price, :condition)
#             RETURNING id
#         """)

#         try:
#             with db.engine.connect() as connection:
#                 result = connection.execute(query, {
#                     'item': data['item'],
#                     'specifications': data['specifications'],
#                     'class_code': data['class_code'],
#                     'serial_no': data['serial_no'],
#                     'purchase_date': purchase_date,  # Pass None if not provided
#                     'depreciation_rate': data['depreciation_rate'],
#                     'vendor': data['vendor'],
#                     'purchase_price': data['purchase_price'],
#                     'condition': data['condition']
#                 })
#                 connection.commit()
#                 asset_id = result.scalar()
#             return {'message': 'Asset added successfully', 'id': asset_id}, 201
#         except IntegrityError as e:
#             return {'message': f'Integrity error: {str(e)}'}, 400
#         except Exception as e:
#             return {'message': f'Error adding asset: {str(e)}'}, 500

# @asset_ns.route('/<int:asset_id>')
# class AssetDetail(Resource):
#     def get(self, asset_id):
#         """
#         Get a single asset by ID, including assignment details
#         """
#         query = text("""
#             SELECT a.id, a.item, a.class_code, a.serial_no, a.purchase_date, 
#                    a.depreciation_rate, a.depreciation_end_date, a.vendor, 
#                    ass.id AS assignment_id, ass.location_id, ass.assigned_to
#             FROM asset a
#             LEFT JOIN assignment ass ON a.id = ass.asset_id
#             WHERE a.id = :id
#         """)

#         with db.engine.connect() as connection:
#             result = connection.execute(query, {'id': asset_id}).mappings().first()
#             if not result:
#                 return {'message': 'Asset not found'}, 404
        
#         asset = {key: (value.isoformat() if isinstance(value, date) else value) for key, value in result.items()}

#         return jsonify({
#             'id': asset.get('id'),
#             'assignment_id': asset.get('assignment_id'),
#             'item': asset.get('item'),
#             'location_id': asset.get('location_id'),  # Location where the asset is assigned
#             'assigned_to': asset.get('assigned_to'),  # Who/what the asset is assigned to
#             'class_code': asset.get('class_code'),
#             'serial_no': asset.get('serial_no'),
#             'purchase_date': asset.get('purchase_date'),
#             'depreciation_rate': asset.get('depreciation_rate'),
#             'depreciation_end_date': asset.get('depreciation_end_date'),
#             'vendor': asset.get('vendor'),
#         })



#     def delete(self, asset_id):
#         """
#         Delete an asset by ID
#         """
#         query = text("DELETE FROM asset WHERE id = :id")
#         with db.engine.connect() as connection:
#             result = connection.execute(query, {'id': asset_id})
#             connection.commit()
#             if result.rowcount == 0:
#                 return {'message': 'Asset not found'}, 404
#         return {'message': 'Asset deleted successfully'}, 204

#     @asset_ns.expect(Asset_model)
#     def put(self, asset_id):
#         """
#         Update an asset by ID
#         """
#         data = request.get_json()
#         update_fields = []
#         update_params = {'id': asset_id}

#         # 🔹 Build dynamic SQL query based on provided fields
#         for field, value in data.items():
#             update_fields.append(f"{field} = :{field}")
#             update_params[field] = value

#         if not update_fields:
#             return {'message': 'No fields provided for update'}, 400

#         query = text(f"""
#             UPDATE asset
#             SET {", ".join(update_fields)}
#             WHERE id = :id
#             RETURNING id
#         """)

#         with db.engine.connect() as connection:
#             result = connection.execute(query, update_params)
#             connection.commit()
#             if result.rowcount == 0:
#                 return {'message': 'Asset not found'}, 404

#         return {'message': 'Asset updated successfully'}, 200

# @asset_ns.route('/filter')
# class AssetFilter(Resource):
#     def post(self):
#         """
#         Get assets based on filters
#         """
#         filters = request.get_json()
#         query = "SELECT * FROM asset WHERE 1=1"
#         params = {}

#         if 'location_id' in filters:
#             query += " AND location_id = :location_id"
#             params['location_id'] = filters['location_id']

#         if 'class_code' in filters:
#             query += " AND class_code = :class_code"
#             params['class_code'] = filters['class_code']

#         if 'depreciation_start_date' in filters:
#             query += " AND depreciation_start_date >= :depreciation_start_date"
#             params['depreciation_start_date'] = filters['depreciation_start_date']

#         if 'depreciation_end_date' in filters:
#             query += " AND depreciation_end_date <= :depreciation_end_date"
#             params['depreciation_end_date'] = filters['depreciation_end_date']

#         with db.engine.connect() as connection:
#             result = connection.execute(text(query), params)
#             assets = [
#                 {key: (value.isoformat() if isinstance(value, date) else value) for key, value in row.items()}
#                 for row in result.mappings()
#             ]

#         if not assets:
#             return {'message': 'No assets found matching the provided filters'}, 200

#         return assets, 200

# def register_routes(api):
#     """
#     Register asset namespace routes
#     """
#     api.add_namespace(asset_ns)










# from flask import request, jsonify
# from flask_restx import Namespace, Resource, fields
# from exts import db
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy import text
# from datetime import date

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
#         'condition': fields.String(required=True, description='Condition')
#     }
# )

# @asset_ns.route('/')
# class AssetList(Resource):
#     def get(self):
#         """
#         Get a list of all assets
#         """
#         query = text("SELECT * FROM asset")
#         with db.engine.connect() as connection:
#             result = connection.execute(query)
#             assets = [
#                 {key: (value.isoformat() if isinstance(value, date) else value) for key, value in row.items()}
#                 for row in result.mappings()
#             ]
#         return assets, 200

#     @asset_ns.expect(Asset_model)
#     def post(self):
#         """
#         Create a new asset
#         """
#         data = request.get_json()
#         purchase_date = data.get('purchase_date') or None  # Defaults to None if not provided

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
#             return {'message': f'Integrity error: {str(e)}'}, 400
#         except Exception as e:
#             return {'message': f'Error adding asset: {str(e)}'}, 500

# @asset_ns.route('/<int:asset_id>')
# class AssetDetail(Resource):
#     def get(self, asset_id):
#         """
#         Get a single asset by ID, including assignment details
#         """
#         query = text("""
#             SELECT a.id, a.item, a.class_code, a.serial_no, a.purchase_date, 
#                    a.depreciation_rate, a.depreciation_end_date, a.vendor, 
#                    ass.id AS assignment_id, ass.location_id, ass.assigned_to, 
#                    loc.name AS location_name
#             FROM asset a
#             LEFT JOIN assignment ass ON a.id = ass.asset_id
#             LEFT JOIN location loc ON ass.location_id = loc.id
#             WHERE a.id = :id
#         """)

#         with db.engine.connect() as connection:
#             result = connection.execute(query, {'id': asset_id}).mappings().first()
#             if not result:
#                 return {'message': 'Asset not found'}, 404
        
#         asset = {key: (value.isoformat() if isinstance(value, date) else value) for key, value in result.items()}

#         return jsonify(asset)

#     def delete(self, asset_id):
#         """
#         Delete an asset by ID
#         """
#         query = text("DELETE FROM asset WHERE id = :id")
#         with db.engine.connect() as connection:
#             result = connection.execute(query, {'id': asset_id})
#             connection.commit()
#             if result.rowcount == 0:
#                 return {'message': 'Asset not found'}, 404
#         return {'message': 'Asset deleted successfully'}, 204

#     @asset_ns.expect(Asset_model)
#     def put(self, asset_id):
#         """
#         Update an asset by ID
#         """
#         data = request.get_json()
#         update_fields = [f"{key} = :{key}" for key in data.keys()]
#         data['id'] = asset_id

#         if not update_fields:
#             return {'message': 'No fields provided for update'}, 400

#         query = text(f"""
#             UPDATE asset
#             SET {', '.join(update_fields)}
#             WHERE id = :id
#             RETURNING id
#         """)

#         with db.engine.connect() as connection:
#             result = connection.execute(query, data)
#             connection.commit()
#             if result.rowcount == 0:
#                 return {'message': 'Asset not found'}, 404

#         return {'message': 'Asset updated successfully'}, 200

# @asset_ns.route('/filter')
# class AssetFilter(Resource):
#     def post(self):
#         """
#         Get assets based on filters
#         """
#         filters = request.get_json()
#         query = "SELECT * FROM asset WHERE 1=1"
#         params = {}

#         if 'location_id' in filters:
#             query += " AND location_id = :location_id"
#             params['location_id'] = filters['location_id']

#         if 'class_code' in filters:
#             query += " AND class_code = :class_code"
#             params['class_code'] = filters['class_code']

#         if 'depreciation_start_date' in filters:
#             query += " AND depreciation_start_date >= :depreciation_start_date"
#             params['depreciation_start_date'] = filters['depreciation_start_date']

#         if 'depreciation_end_date' in filters:
#             query += " AND depreciation_end_date <= :depreciation_end_date"
#             params['depreciation_end_date'] = filters['depreciation_end_date']

#         with db.engine.connect() as connection:
#             result = connection.execute(text(query), params)
#             assets = [
#                 {key: (value.isoformat() if isinstance(value, date) else value) for key, value in row.items()}
#                 for row in result.mappings()
#             ]

#         return assets if assets else {'message': 'No assets found matching the provided filters'}, 200

# def register_routes(api):
#     """
#     Register asset namespace routes
#     """
#     api.add_namespace(asset_ns)








# from flask import request, jsonify
# from flask_restx import Namespace, Resource, fields
# from exts import db
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy import text
# from datetime import date

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
#         'location_id': fields.Integer(description='Location ID of the asset'),
#         'location_name': fields.String(description='Location Name of the asset')
#     }
# )

# @asset_ns.route('/')
# class AssetList(Resource):
#     def get(self):
#         """Get a list of all assets, including their locations."""
#         query = text("""
#             SELECT a.*, l.name AS location_name 
#             FROM asset a
#             LEFT JOIN location l ON a.location_id = l.id
#         """)

#         with db.engine.connect() as connection:
#             result = connection.execute(query)
#             assets = [
#                 {key: (value.isoformat() if isinstance(value, date) else value) for key, value in row.items()}
#                 for row in result.mappings()
#             ]
#         return assets, 200

#     @asset_ns.expect(Asset_model)
#     def post(self):
#         """Create a new asset"""
#         data = request.get_json()
#         purchase_date = data.get('purchase_date') or None  

#         query = text("""
#             INSERT INTO asset (item, specifications, class_code, serial_no, purchase_date, 
#                               depreciation_rate, vendor, purchase_price, condition, location_id)
#             VALUES (:item, :specifications, :class_code, :serial_no, :purchase_date,  
#                     :depreciation_rate, :vendor, :purchase_price, :condition, :location_id)
#             RETURNING id
#         """)

#         try:
#             with db.engine.connect() as connection:
#                 result = connection.execute(query, data)
#                 connection.commit()
#                 asset_id = result.scalar()
#             return {'message': 'Asset added successfully', 'id': asset_id}, 201
#         except IntegrityError as e:
#             return {'message': f'Integrity error: {str(e)}'}, 400
#         except Exception as e:
#             return {'message': f'Error adding asset: {str(e)}'}, 500

# @asset_ns.route('/<int:asset_id>')
# class AssetDetail(Resource):
#     def get(self, asset_id):
#         """Get a single asset by ID, including location details"""
#         query = text("""
#             SELECT a.id, a.item, a.class_code, a.serial_no, a.purchase_date, 
#                    a.depreciation_rate, a.depreciation_end_date, a.vendor, 
#                    a.location_id, l.name AS location_name 
#             FROM asset a
#             LEFT JOIN location l ON a.location_id = l.id  
#             WHERE a.id = :id
#         """)

#         with db.engine.connect() as connection:
#             result = connection.execute(query, {'id': asset_id}).mappings().first()
#             if not result:
#                 return {'message': 'Asset not found'}, 404
        
#         asset = {key: (value.isoformat() if isinstance(value, date) else value) for key, value in result.items()}

#         return jsonify(asset)

#     def delete(self, asset_id):
#         """Delete an asset by ID"""
#         query = text("DELETE FROM asset WHERE id = :id")
#         with db.engine.connect() as connection:
#             result = connection.execute(query, {'id': asset_id})
#             connection.commit()
#             if result.rowcount == 0:
#                 return {'message': 'Asset not found'}, 404
#         return {'message': 'Asset deleted successfully'}, 204

#     @asset_ns.expect(Asset_model)
#     def put(self, asset_id):
#         """Update an asset by ID"""
#         data = request.get_json()
#         update_fields = [f"{key} = :{key}" for key in data.keys()]
#         data['id'] = asset_id

#         if not update_fields:
#             return {'message': 'No fields provided for update'}, 400

#         query = text(f"""
#             UPDATE asset
#             SET {', '.join(update_fields)}
#             WHERE id = :id
#             RETURNING id
#         """)

#         with db.engine.connect() as connection:
#             result = connection.execute(query, data)
#             connection.commit()
#             if result.rowcount == 0:
#                 return {'message': 'Asset not found'}, 404

#         return {'message': 'Asset updated successfully'}, 200

# @asset_ns.route('/filter')
# class AssetFilter(Resource):
#     def post(self):
#         """Get assets based on filters"""
#         filters = request.get_json()
#         query = "SELECT * FROM asset WHERE 1=1"
#         params = {}

#         if 'location_id' in filters:
#             query += " AND location_id = :location_id"
#             params['location_id'] = filters['location_id']

#         if 'class_code' in filters:
#             query += " AND class_code = :class_code"
#             params['class_code'] = filters['class_code']

#         if 'depreciation_start_date' in filters:
#             query += " AND depreciation_start_date >= :depreciation_start_date"
#             params['depreciation_start_date'] = filters['depreciation_start_date']

#         if 'depreciation_end_date' in filters:
#             query += " AND depreciation_end_date <= :depreciation_end_date"
#             params['depreciation_end_date'] = filters['depreciation_end_date']

#         with db.engine.connect() as connection:
#             result = connection.execute(text(query), params)
#             assets = [
#                 {key: (value.isoformat() if isinstance(value, date) else value) for key, value in row.items()}
#                 for row in result.mappings()
#             ]

#         return assets if assets else {'message': 'No assets found matching the provided filters'}, 200

# def register_routes(api):
#     """Register asset namespace routes"""
#     api.add_namespace(asset_ns)







from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from exts import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from datetime import date

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
        'location_id': fields.Integer(description='Location ID of the asset'),
        'location_name': fields.String(description='Location Name of the asset')
    }
)

@asset_ns.route('/')
class AssetList(Resource):
    def get(self):
        """Get a list of all assets, including their locations."""
        query = text("""
            SELECT a.*, l.name AS location_name 
            FROM asset a
            LEFT JOIN location l ON a.location_id = l.id
        """)

        with db.engine.connect() as connection:
            result = connection.execute(query)
            assets = [
                {key: (value.isoformat() if isinstance(value, date) else value) for key, value in row.items()}
                for row in result.mappings()
            ]
        return assets, 200

    @asset_ns.expect(Asset_model)
    def post(self):
        """Create a new asset"""
        data = request.get_json()
        purchase_date = data.get('purchase_date') or date.today().isoformat()
        data['purchase_date'] = purchase_date

        query = text("""
            INSERT INTO asset (item, specifications, class_code, serial_no, purchase_date, 
                              depreciation_rate, vendor, purchase_price, condition, location_id)
            VALUES (:item, :specifications, :class_code, :serial_no, :purchase_date,  
                    :depreciation_rate, :vendor, :purchase_price, :condition, :location_id)
            RETURNING id
        """)

        try:
            with db.engine.connect() as connection:
                result = connection.execute(query, data)
                connection.commit()
                asset_id = result.scalar()
            return {'message': 'Asset added successfully', 'id': asset_id}, 201
        except IntegrityError as e:
            return {'message': f'Integrity error: {str(e)}'}, 400
        except Exception as e:
            return {'message': f'Error adding asset: {str(e)}'}, 500

@asset_ns.route('/<int:asset_id>')
class AssetDetail(Resource):
    def get(self, asset_id):
        """Get a single asset by ID, including location details"""
        query = text("""
            SELECT a.*, l.name AS location_name 
            FROM asset a
            LEFT JOIN location l ON a.location_id = l.id  
            WHERE a.id = :id
        """)

        with db.engine.connect() as connection:
            result = connection.execute(query, {'id': asset_id}).mappings().first()
            if not result:
                return {'message': 'Asset not found'}, 404
        
        asset = {key: (value.isoformat() if isinstance(value, date) else value) for key, value in result.items()}
        return jsonify(asset)

    def delete(self, asset_id):
        """Delete an asset by ID"""
        query = text("DELETE FROM asset WHERE id = :id")
        with db.engine.connect() as connection:
            result = connection.execute(query, {'id': asset_id})
            connection.commit()
            if result.rowcount == 0:
                return {'message': 'Asset not found'}, 404
        return {'message': 'Asset deleted successfully'}, 204

    @asset_ns.expect(Asset_model)
    def put(self, asset_id):
        """Update an asset by ID"""
        data = request.get_json()
        update_fields = [f"{key} = :{key}" for key in data.keys()]
        data['id'] = asset_id

        if not update_fields:
            return {'message': 'No fields provided for update'}, 400

        query = text(f"""
            UPDATE asset
            SET {', '.join(update_fields)}
            WHERE id = :id
            RETURNING id
        """)

        with db.engine.connect() as connection:
            result = connection.execute(query, data)
            connection.commit()
            if result.rowcount == 0:
                return {'message': 'Asset not found'}, 404

        return {'message': 'Asset updated successfully'}, 200

def register_routes(api):
    """Register asset namespace routes"""
    api.add_namespace(asset_ns)
