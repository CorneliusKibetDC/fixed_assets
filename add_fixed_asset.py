from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from models import Asset, Location
from app import db

asset_ns = Namespace('assets', description='Asset operations')

Asset_model = asset_ns.Model(
    'Asset',
    {
        'item': fields.String(required=True, description='Item name'),
       'specifications': fields.String(required=True, description='Specifications'),
        'class_code': fields.String(required=True, description='Class code'),
       'serial_no': fields.String(required=True, description='Serial number'),
        'purchase_date': fields.Date(required=True, description='Purchase date'),
        'location_id': fields.Integer(required=True, description='Location ID'),
        'depreciation_rate': fields.Float(required=True, description='Depreciation rate'),
       'vendor': fields.String(required=True, description='Vendor'),
        'purchase_price': fields.Float(required=True, description='Purchase price'),
        'condition': fields.String(required=True, description='Condition')
    }
)

@asset_ns.route('/assets')
class AssetList(Resource):
   
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



