# from flask import request, jsonify
# from app import app
# #from app.models import Asset
# #from flask_jwt_extended import jwt_required

# mock_assets = []
# @app.route('/assets', methods=['POST'])
# def add_asset():
#     data = request.json
#     new_asset = {
#         'item': data['item'],
#         'specifications': data['specifications'],
#         'class_code': data['class_code'],
#         'serial_no': data['serial_no'],
#         'purchase_date': data['purchase_date'],
#         'location': data['location'],
#         'depreciation_rate': data['depreciation_rate'],
#         'vendor': data['vendor'],
#         'purchase_price': data['purchase_price'],
#         'condition': data['condition']
#     }
    
#     mock_assets.append(new_asset)
#     # db.session.add(new_asset)
#     # db.session.commit()
    
#     return jsonify({'message': 'Asset added successfully',
#                     'asset':new_asset
#                     }), 201
        
        
        
        
        
        
        
        
# from flask import request, jsonify
# from flask_restx import Namespace, Resource
# from flask_jwt_extended import jwt_required
# from models import Asset
# from app import db

# asset_ns = Namespace('assets', description='Asset operations')

# @asset_ns.route('/')
# class AssetList(Resource):
#     #@jwt_required()
#     def post(self):
#         data = request.json
        
#         required_fields = [
#             'item', 'specifications', 'class_code', 'serial_no',
#             'purchase_date', 'location', 'depreciation_rate',
#             'vendor', 'purchase_price', 'condition'
#         ]
        
#         for field in required_fields:
#             if field not in data:
#                 return {'message': f'Missing field: {field}'}, 400
        
#         new_asset = Asset(
#             item=data['item'],
#             specifications=data['specifications'],
#             class_code=data['class_code'],
#             serial_no=data['serial_no'],
#             purchase_date=data['purchase_date'],
#             location=data['location'],
#             depreciation_rate=data['depreciation_rate'],
#             vendor=data['vendor'],
#             purchase_price=data['purchase_price'],
#             condition=data['condition']
#         )
        
#         try:
#             db.session.add(new_asset)
#             db.session.commit()
#             return jsonify({'message': 'Asset added successfully', 'asset': new_asset.to_dict()}), 201
#         except Exception as e:
#             db.session.rollback()
#             return {'message': str(e)}, 500

# def register_routes(api):
#     api.add_namespace(asset_ns)






# from flask import request, jsonify
# from flask_restx import Namespace, Resource
# from flask_jwt_extended import jwt_required
# from models import Asset, Location  # Import Location model
# from app import db
# #from flask import current_app

# asset_ns = Namespace('assets', description='Asset operations')

# @asset_ns.route('/')
# class AssetList(Resource):
#     # @jwt_required()
#     def post(self):
#         data = request.json
        
#         required_fields = [
#             'item', 'specifications', 'class_code', 'serial_no',
#             'purchase_date', 'location_id', 'depreciation_rate',
#             'vendor', 'purchase_price', 'condition'
#         ]
        
#         # Check for missing fields
#         for field in required_fields:
#             if field not in data:
#                 return {'message': f'Missing field: {field}'}, 400
        
#         # Validate location_id
#         location = Location.query.get(data['location_id'])
#         if not location:
#             return {'message': 'Invalid location_id provided'}, 400

#         # Create new Asset
#         new_asset = Asset(
#             item=data['item'],
#             specifications=data['specifications'],
#             class_code=data['class_code'],
#             serial_no=data['serial_no'],
#             purchase_date=data['purchase_date'],
#             location_id=location.id,  # Use location_id here
#             depreciation_rate=data['depreciation_rate'],
#             vendor=data['vendor'],
#             purchase_price=data['purchase_price'],
#             condition=data['condition']
#         )
        
#         try:
#             db.session.add(new_asset)
#             db.session.commit()
#             return jsonify({'message': 'Asset added successfully', 'asset': new_asset.to_dict()}), 201
#         except Exception as e:
#             db.session.rollback()
#             return {'message': str(e)}, 500

# def register_routes(api):
#     api.add_namespace(asset_ns)







from flask import request, jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from models import Asset, Location
from app import db

asset_ns = Namespace('assets', description='Asset operations')

@asset_ns.route('/')
class AssetList(Resource):
    #@jwt_required()  # Uncomment if JWT is configured
    def post(self):
        data = request.json

        required_fields = [
            'item', 'specifications', 'class_code', 'serial_no',
            'purchase_date', 'location_id', 'depreciation_rate',
            'vendor', 'purchase_price', 'condition'
        ]
        
        # Check for missing fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return {'message': f'Missing fields: {", ".join(missing_fields)}'}, 400
        
        # Query without extra app_context
        location = Location.query.get(data['location_id'])
        if not location:
            return {'message': 'Invalid location_id provided'}, 400

        # Create new Asset
        new_asset = Asset(
            item=data['item'],
            specifications=data['specifications'],
            class_code=data['class_code'],
            serial_no=data['serial_no'],
            purchase_date=data['purchase_date'],
            location_id=location.id,
            depreciation_rate=data['depreciation_rate'],
            vendor=data['vendor'],
            purchase_price=data['purchase_price'],
            condition=data['condition']
        )
        
        try:
            db.session.add(new_asset)
            db.session.commit()
            return jsonify({'message': 'Asset added successfully', 'asset': new_asset.to_dict()}), 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error adding asset: {str(e)}'}, 500

def register_routes(api):
    api.add_namespace(asset_ns)


