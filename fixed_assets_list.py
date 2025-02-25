# from flask import jsonify
# from app import app
# from models import Asset
# from flask_jwt_extended import jwt_required
# @app.route("/assets", methods=["GET",])
# @jwt_required()
# def get_assets():
#     assets = Asset.query.all()
#     return jsonify([asset.to_dict() for asset in assets])









# from flask import jsonify
# from flask_restx import Namespace, Resource
# from models import Asset
# from flask_jwt_extended import jwt_required

# # Create a namespace for assets
# asset_ns = Namespace('assets', description='Asset operations')

# @asset_ns.route('/')
# class AssetList(Resource):
#     #@jwt_required()
#     def get(self):
#         assets = Asset.query.all()
#         return jsonify([asset.to_dict() for asset in assets])

# # Register the namespace in your main app file
# def register_routes(api):
#     api.add_namespace(asset_ns)








from flask import jsonify
from flask_restx import Namespace, Resource
from models import Asset
from flask_jwt_extended import jwt_required

# Create a namespace for assets
asset_ns = Namespace('assets', description='Asset operations')

@asset_ns.route('/')
class AssetList(Resource):
    #@jwt_required()
    def get(self):
        try:
            assets = Asset.query.all()
            return jsonify([asset.to_dict() for asset in assets]), 200
        except Exception as e:
            return jsonify({'message': f'Error fetching assets: {str(e)}'}), 500

# Register the namespace in your main app file
def register_routes(api):
    api.add_namespace(asset_ns)