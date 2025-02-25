# from flask import request, jsonify
# from app import app
# from models import Asset
# from flask_jwt_extended import jwt_required

# @app.route('/assets/filter', methods=['POST'])
# @jwt_required
# def get_assets():
#     filters = request.get_json()
#     query = Asset.query
#     if 'location' in filters:
#         query = query.filter_by(location=filters['location'])
#     if 'status' in filters:
#         query = query.filter_by(status=filters['status'])
#     if 'depreciation_start_date' in filters:
#         query = query.filter(Asset.depreciation_start_date >= filters['depreciation_start_date'])
#     if 'depreciation_end_date' in filters:
#         query = query.filter(Asset.depreciation_end_date <= filters['depreciation_end_date'])
        
#     assets = query.all()
#     return jsonify([asset.serialize() for asset in assets])           
    
    
    




# from flask import request, jsonify
# from flask_restx import Namespace, Resource
# from flask_jwt_extended import jwt_required
# from models import Asset

# filter_asset_ns = Namespace('assets', description='Asset filtering operations')

# @filter_asset_ns.route('/filter')
# class FilterAssets(Resource):
#     @jwt_required()
#     def post(self):
#         filters = request.get_json()
#         query = Asset.query
        
#         if 'location' in filters:
#             query = query.filter_by(location=filters['location'])
#         if 'status' in filters:
#             query = query.filter_by(status=filters['status'])
#         if 'depreciation_start_date' in filters:
#             query = query.filter(Asset.depreciation_start_date >= filters['depreciation_start_date'])
#         if 'depreciation_end_date' in filters:
#             query = query.filter(Asset.depreciation_end_date <= filters['depreciation_end_date'])
        
#         assets = query.all()
#         return jsonify([asset.to_dict() for asset in assets])

# def register_routes(api):
#     api.add_namespace(filter_asset_ns)







from flask import request, jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from models import Asset

filter_asset_ns = Namespace('assets', description='Asset filtering operations')

@filter_asset_ns.route('/filter')
class FilterAssets(Resource):
    #@jwt_required()
    def post(self):
        filters = request.get_json()
        query = Asset.query
        
        if 'location' in filters:
            query = query.filter_by(location=filters['location'])
        if 'status' in filters:
            query = query.filter_by(status=filters['status'])
        if 'depreciation_start_date' in filters:
            query = query.filter(Asset.depreciation_start_date >= filters['depreciation_start_date'])
        if 'depreciation_end_date' in filters:
            query = query.filter(Asset.depreciation_end_date <= filters['depreciation_end_date'])
        
        assets = query.all()
        return jsonify([asset.to_dict() for asset in assets])

def register_routes(api):
    api.add_namespace(filter_asset_ns)
