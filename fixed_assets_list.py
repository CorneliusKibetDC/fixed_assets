from flask import jsonify
from app import app
from models import Asset
from flask_jwt_extended import jwt_required
@app.route("/assets", methods=["GET",])
@jwt_required()
def get_assets():
    assets = Asset.query.all()
    return jsonify([asset.to_dict() for asset in assets])


    
    