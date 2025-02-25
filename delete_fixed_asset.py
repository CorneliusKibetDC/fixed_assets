# from flask import jsonify
# from app import app, db
# from models import Asset
# from flask_jwt_extended import jwt_required

# @app.route('/assets/<int:id>', methods=['DELETE'])
# @jwt_required
# def delete_asset(id):
#     asset = Asset.query.get(id)
#     if asset:
#         db.session.delete(asset)
#         db.session.commit()
#         return jsonify({'message': 'Asset deleted successfully'})
#     return jsonify({'message':"Asset not found"}), 404




# from flask import request, jsonify
# from flask_restx import Namespace, Resource
# from flask_jwt_extended import jwt_required
# from models import Asset
# from app import db

# delete_asset_ns = Namespace('delete_asset', description='Asset deletion operations')

# @delete_asset_ns.route('/delete/<int:asset_id>')
# class DeleteAsset(Resource):
#     #@jwt_required()
#     def delete(self, asset_id):
#         asset = Asset.query.get(asset_id)
#         if not asset:
#             return jsonify({'message': 'Asset not found'}), 404

#         db.session.delete(asset)
#         db.session.commit()
#         return jsonify({'message': 'Asset deleted successfully'})

# def register_routes(api):
#     api.add_namespace(delete_asset_ns)






from flask import request, jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from models import Asset
from app import db

delete_asset_ns = Namespace('delete_asset', description='Asset deletion operations')

@delete_asset_ns.route('/delete/<int:asset_id>')
class DeleteAsset(Resource):
    #@jwt_required()
    def delete(self, asset_id):
        asset = Asset.query.get(asset_id)
        if not asset:
            return jsonify({'message': 'Asset not found'}), 404

        db.session.delete(asset)
        db.session.commit()
        return jsonify({'message': 'Asset deleted successfully'})

def register_routes(api):
    api.add_namespace(delete_asset_ns)

