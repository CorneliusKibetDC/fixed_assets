from flask import jsonify
from app import app, db
from models import Asset
from flask_jwt_extended import jwt_required

@app.route('/assets/<int:id>', methods=['DELETE'])
@jwt_required
def delete_asset(id):
    asset = Asset.query.get(id)
    if asset:
        db.session.delete(asset)
        db.session.commit()
        return jsonify({'message': 'Asset deleted successfully'})
    return jsonify({'message':"Asset not found"}), 404