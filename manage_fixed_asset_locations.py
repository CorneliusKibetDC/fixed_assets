# from flask import Blueprint, request, jsonify
# from app import db
# from models import Location, Asset, Assignment  # Import Assignment model to get asset quantities

# # Create a Blueprint for the location management
# location_bp = Blueprint('location', __name__)

# @location_bp.route('/locations', methods=['POST'])
# def create_location():
#     data = request.get_json()
    
#     # Validate input
#     name = data.get('name')
#     description = data.get('description')

#     if not name:
#         return jsonify({'error': 'Name field is required'}), 400

#     # Create a new location
#     new_location = Location(
#         name=name,
#         description=description
#     )

#     db.session.add(new_location)
#     db.session.commit()

#     return jsonify(new_location.to_dict()), 201

# @location_bp.route('/locations/<int:location_id>', methods=['GET'])
# def get_location(location_id):
#     location = Location.query.get_or_404(location_id)
    
#     # Fetch assets assigned to this location
#     assets = Assignment.query.filter_by(location_id=location.id).all()
#     asset_details = [
#         {
#             'asset_id': assignment.asset_id,
#             'assigned_to': assignment.assigned_to,
#             'quantity': 1  # Assuming each assignment represents one asset
#         }
#         for assignment in assets
#     ]

#     location_info = location.to_dict()
#     location_info['assets'] = asset_details  # Add assets to location info

#     return jsonify(location_info)

# @location_bp.route('/locations/<int:location_id>', methods=['PUT'])
# def update_location(location_id):
#     location = Location.query.get_or_404(location_id)
#     data = request.get_json()

#     # Update fields from the request
#     if 'name' in data:
#         location.name = data['name']
#     if 'description' in data:
#         location.description = data['description']

#     db.session.commit()
#     return jsonify(location.to_dict())

# @location_bp.route('/locations/<int:location_id>', methods=['DELETE'])
# def delete_location(location_id):
#     location = Location.query.get_or_404(location_id)
#     db.session.delete(location)
#     db.session.commit()
#     return jsonify({'message': 'Location deleted successfully'}), 204

# @location_bp.route('/locations', methods=['GET'])
# def get_locations():
#     locations = Location.query.all()
#     location_list = []
    
#     for location in locations:
#         # Fetch assets assigned to each location
#         assets = Assignment.query.filter_by(location_id=location.id).all()
#         asset_details = [
#             {
#                 'asset_id': assignment.asset_id,
#                 'assigned_to': assignment.assigned_to,
#                 'quantity': 1  # Each assignment represents one asset
#             }
#             for assignment in assets
#         ]
        
#         location_info = location.to_dict()
#         location_info['assets'] = asset_details  # Add assets to location info
#         location_list.append(location_info)

#     return jsonify(location_list)

# # Register the blueprint in your app
# def register_routes(app):
#     app.register_blueprint(location_bp)












### manage_fixed_asset_locations.py

# from flask import request, jsonify
# from flask_restx import Namespace, Resource
# from app import db
# from models import Location, Assignment
# from flask_jwt_extended import jwt_required

# # Create a namespace for location management
# location_ns = Namespace('locations', description='Location operations')

# @location_ns.route('/')
# class LocationList(Resource):
#     #@jwt_required()
#     def post(self):
#         data = request.get_json()
        
#         # Validate input
#         name = data.get('name')
#         description = data.get('description')

#         if not name:
#             return jsonify({'error': 'Name field is required'}), 400

#         # Create a new location
#         new_location = Location(
#             name=name,
#             description=description
#         )

#         db.session.add(new_location)
#         db.session.commit()

#         return jsonify(new_location.to_dict()), 201

#     #@jwt_required()
#     def get(self):
#         locations = Location.query.all()
#         location_list = []
        
#         for location in locations:
#             assets = Assignment.query.filter_by(location_id=location.id).all()
#             asset_details = [
#                 {
#                     'asset_id': assignment.asset_id,
#                     'assigned_to': assignment.assigned_to,
#                     'quantity': 1  # Each assignment represents one asset
#                 }
#                 for assignment in assets
#             ]
            
#             location_info = location.to_dict()
#             location_info['assets'] = asset_details
#             location_list.append(location_info)

#         return jsonify(location_list), 200

# @location_ns.route('/<int:location_id>')
# class LocationResource(Resource):
#     #@jwt_required()
#     def get(self, location_id):
#         location = Location.query.get_or_404(location_id)
        
#         assets = Assignment.query.filter_by(location_id=location.id).all()
#         asset_details = [
#             {
#                 'asset_id': assignment.asset_id,
#                 'assigned_to': assignment.assigned_to,
#                 'quantity': 1  # Assuming each assignment represents one asset
#             }
#             for assignment in assets
#         ]

#         location_info = location.to_dict()
#         location_info['assets'] = asset_details

#         return jsonify(location_info), 200

#     #@jwt_required()
#     def put(self, location_id):
#         location = Location.query.get_or_404(location_id)
#         data = request.get_json()

#         # Update fields from the request
#         if 'name' in data:
#             location.name = data['name']
#         if 'description' in data:
#             location.description = data['description']

#         db.session.commit()
#         return jsonify(location.to_dict()), 200

#     #@jwt_required()
#     def delete(self, location_id):
#         location = Location.query.get_or_404(location_id)
#         db.session.delete(location)
#         db.session.commit()
#         return jsonify({'message': 'Location deleted successfully'}), 204

# # Register the namespace in your app
# def register_routes(api):
#     api.add_namespace(location_ns)









from flask import request, jsonify
from flask_restx import Namespace, Resource
from app import db
from models import Location, Assignment
from flask_jwt_extended import jwt_required

# Create a namespace for location management
location_ns = Namespace('locations', description='Location operations')

@location_ns.route('/')
class LocationList(Resource):
    #@jwt_required()
    def post(self):
        data = request.get_json()
        
        # Validate input
        name = data.get('name')
        description = data.get('description')

        if not name:
            return jsonify({'error': 'Name field is required'}), 400

        # Create a new location
        new_location = Location(
            name=name,
            description=description
        )

        db.session.add(new_location)
        db.session.commit()

        return jsonify(new_location.to_dict()), 201

    #@jwt_required()
    def get(self):
        locations = Location.query.all()
        location_list = []
        
        for location in locations:
            assets = Assignment.query.filter_by(location_id=location.id).all()
            asset_details = [
                {
                    'asset_id': assignment.asset_id,
                    'assigned_to': assignment.assigned_to,
                    'quantity': 1  # Each assignment represents one asset
                }
                for assignment in assets
            ]
            
            location_info = location.to_dict()
            location_info['assets'] = asset_details
            location_list.append(location_info)

        return jsonify(location_list), 200

@location_ns.route('/<int:location_id>')
class LocationResource(Resource):
    #@jwt_required()
    def get(self, location_id):
        location = Location.query.get_or_404(location_id)
        
        assets = Assignment.query.filter_by(location_id=location.id).all()
        asset_details = [
            {
                'asset_id': assignment.asset_id,
                'assigned_to': assignment.assigned_to,
                'quantity': 1  # Assuming each assignment represents one asset
            }
            for assignment in assets
        ]

        location_info = location.to_dict()
        location_info['assets'] = asset_details

        return jsonify(location_info), 200

    #@jwt_required()
    def put(self, location_id):
        location = Location.query.get_or_404(location_id)
        data = request.get_json()

        # Update fields from the request
        if 'name' in data:
            location.name = data['name']
        if 'description' in data:
            location.description = data['description']

        db.session.commit()
        return jsonify(location.to_dict()), 200

    #@jwt_required()
    def delete(self, location_id):
        location = Location.query.get_or_404(location_id)
        db.session.delete(location)
        db.session.commit()
        return jsonify({'message': 'Location deleted successfully'}), 204

# Register the namespace in your app
def register_routes(api):
    api.add_namespace(location_ns)
