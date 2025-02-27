










from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app import db
from models import Location, Assignment
from sqlalchemy.orm import joinedload
# from flask_jwt_extended import jwt_required  # Uncomment when needed

# Create a namespace for location management
location_ns = Namespace('locations', description='Location operations')

# Define API Model for input validation and documentation
Location_model = location_ns.model(
    'Location',
    {
        'name': fields.String(required=True, description='Name of the location'),
        'description': fields.String(required=False, description='Description of the location')
    }
)

@location_ns.route('/')
class LocationList(Resource):
    # @jwt_required()
    @location_ns.expect(Location_model)
    def post(self):
        data = request.get_json()
        
        # Create a new location using direct assignment
        new_location = Location(**data)
        db.session.add(new_location)
        db.session.commit()

        return new_location.to_dict(), 201

    # @jwt_required()
    def get(self):
        locations = Location.query.options(joinedload(Location.assets)).all()
        location_list = []
        
        for location in locations:
            asset_details = [
                {'asset_id': a.asset_id, 'assigned_to': a.assigned_to}
                for a in location.assignments
            ]
            
            location_info = location.to_dict()
            location_info['assets'] = asset_details
            location_list.append(location_info)

        return location_list, 200

@location_ns.route('/<int:location_id>')
class LocationResource(Resource):
    # @jwt_required()
    def get(self, location_id):
        location = Location.query.options(joinedload(Location.assets)).filter_by(id=location_id).first_or_404()
        
        asset_details = [
            {'asset_id': a.asset_id, 'assigned_to': a.assigned_to}
            for a in location.assignments
        ]

        location_info = location.to_dict()
        location_info['assets'] = asset_details

        return location_info, 200

    # @jwt_required()
    @location_ns.expect(Location_model)
    def put(self, location_id):
        location = Location.query.get_or_404(location_id)
        data = request.get_json()

        # Update fields dynamically
        for key, value in data.items():
            setattr(location, key, value)
        
        db.session.commit()
        return location.to_dict(), 200

    # @jwt_required()
    def delete(self, location_id):
        location = Location.query.get_or_404(location_id)
        db.session.delete(location)
        db.session.commit()
        return '', 204  # No content for 204 response

# Register the namespace in your app
def register_routes(api):
    api.add_namespace(location_ns)
