from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from models import Asset, Location
from exts import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# Define the Namespace for 'assets' API operations
asset_ns = Namespace('assets', description='Asset operations')

# Define the Asset Model for serialization
Asset_model = asset_ns.model(
    'Asset',
    {
        'item': fields.String(required=True, description='Item name'),
        'id': fields.String(description='Asset id'),
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
    @asset_ns.marshal_list_with(Asset_model)
    def get(self):
        """
        Get a list of all assets
        """
        assets = Asset.query.all()
        return assets, 200
    
    @asset_ns.expect(Asset_model)
    @asset_ns.marshal_with(Asset_model, code=201)
    def post(self):
        """
        Create a new asset
        """
        data = request.get_json()
        print(f"Received Data: {data}")

        # Validate location_id
        location = Location.query.get(data['location_id'])
        if not location:
            return {'message': 'Invalid location_id provided'}, 400

        # Manually format purchase_date as date object
        try:
            purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date()
        except ValueError:
            return {'message': 'Invalid date format for purchase_date'}, 400
        
        # Create new Asset
        new_asset = Asset(
            item=data['item'],
            specifications=data['specifications'],
            class_code=data['class_code'],
            serial_no=data['serial_no'],
            purchase_date=purchase_date,
            location_id=data['location_id'],
            depreciation_rate=data['depreciation_rate'],
            depreciation_start_date=data['depreciation_start_date'],
            depreciation_end_date=data['depreciation_end_date'],
            vendor=data['vendor'],
            purchase_price=data['purchase_price'],
            condition=data['condition'],
            status = data['status']
        )
        
        try:
            db.session.add(new_asset)
            db.session.commit()
            return jsonify({'message': 'Asset added successfully', 'asset': new_asset.to_dict()}), 201
        except IntegrityError as e:
            db.session.rollback()
            return {'message': f'Integrity error: {str(e)}'}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error adding asset: {str(e)}'}, 500

@asset_ns.route('/assets/assets/<int:id>')  # Ensure the route includes the ID parameter
class AssetDetail(Resource):
    @asset_ns.expect(Asset_model)
    @asset_ns.marshal_with(Asset_model, code=200)
    def put(self, id):
        print(f"PUT request received for asset ID: {id}")
        
    
        # Fetch the asset by ID
        asset = Asset.query.get(id)
        if not asset:
            print("Asset not found")
            return {'message': 'Asset not found'}, 404

        # Get data from the request body
        data = request.get_json()
        print(f"Data received: {data}")
        
        # Validate location_id
        location = Location.query.get(data['location_id'])
        if data.get('location_id') and not location:
            return {'message': 'Invalid location_id provided'}, 400
        
        if 'purchase_date' in data:
            try:
                purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date()
                asset.purchase_date = purchase_date
            except ValueError:
                return {'message': 'Invalid date format for purchase_date'}, 400

        # Update the asset fields with the data
        for key, value in data.items():
            if key != 'id':
                setattr(asset, key, value)

        try:
            db.session.commit()
            return jsonify({'message': 'Asset updated successfully', 'asset': asset.to_dict()}), 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error updating asset: {str(e)}'}, 500
        

    def delete(self, id):
        """
        Delete an asset by id
        """
        asset = Asset.query.get_or_404(id)
        if not asset:
            return {'message': 'Asset not found'}, 404

        db.session.delete(asset)
        db.session.commit()
        return {'message': 'Asset deleted successfully'}, 204

@asset_ns.route('/assets/filter', methods=['POST'])
class AssetFilter(Resource):
    def post(self):
        """
        Get assets based on filters
        """
        filters = request.get_json()
        query = Asset.query

        if 'location' in filters:
            location = filters['location']
            location_obj = Location.query.get(location)
            if not location_obj:
                return {'message': 'Invalid location provided'}, 400
            query = query.filter_by(location_id=location)
            
        if 'status' in filters:
            query = query.filter_by(status=filters['status'])
            
        if 'depreciation_start_date' in filters:
            try:
                depreciation_start_date = datetime.strptime(filters['depreciation_start_date'], '%Y-%m-%d').date()
                query = query.filter(Asset.depreciation_start_date >= depreciation_start_date)
            except ValueError:
                return {'message': 'Invalid date format for depreciation_start_date'}, 400
           
        if 'depreciation_end_date' in filters:
            try:
                depreciation_end_date = datetime.strptime(filters['depreciation_end_date'], '%Y-%m-%d').date()
                query = query.filter(Asset.depreciation_end_date <= depreciation_end_date)
            except ValueError:
                return {'message': 'Invalid date format for depreciation_end_date'}, 400
        
        assets = query.all()
        
        if not assets:
            return {'message': 'No assets found matching the provided filters'}
        
        return jsonify([asset.to_dict() for asset in assets])

def register_routes(api):
    """
    Register asset namespace routes
    """
    api.add_namespace(asset_ns)
