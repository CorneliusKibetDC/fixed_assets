from flask import request, jsonify
from app import app
#from app.models import Asset
#from flask_jwt_extended import jwt_required

mock_assets = []
@app.route('/assets', methods=['POST'])
def add_asset():
    data = request.json
    new_asset = {
        'item': data['item'],
        'specifications': data['specifications'],
        'class_code': data['class_code'],
        'serial_no': data['serial_no'],
        'purchase_date': data['purchase_date'],
        'location': data['location'],
        'depreciation_rate': data['depreciation_rate'],
        'vendor': data['vendor'],
        'purchase_price': data['purchase_price'],
        'condition': data['condition']
    }
    
    mock_assets.append(new_asset)
    # db.session.add(new_asset)
    # db.session.commit()
    
    return jsonify({'message': 'Asset added successfully',
                    'asset':new_asset
                    }), 201
        