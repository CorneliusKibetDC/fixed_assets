
from flask import jsonify
from flask_restx import Namespace, Resource,fields
from models import Asset
from flask_jwt_extended import jwt_required

# Create a namespace for assets
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

@asset_ns.route('/')
class AssetList(Resource):
    
    def get(self):
        try:
            assets = Asset.query.all()
            return jsonify([asset.to_dict() for asset in assets]), 200
        except Exception as e:
            return jsonify({'message': f'Error fetching assets: {str(e)}'}), 500

# Register the namespace in your main app file
def register_routes(api):
    api.add_namespace(asset_ns)