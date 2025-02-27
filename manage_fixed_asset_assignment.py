








from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app import db
from models import Asset, Location, Assignment
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import joinedload
from datetime import datetime

# Create a namespace for assignments
assignment_ns = Namespace('assignments', description='Asset assignment operations')

# Define API Model for input validation and documentation
Assignment_model = assignment_ns.model(
    'Assignment',
    {
        'asset_id': fields.Integer(required=True, description='ID of the assigned asset'),
        'location_id': fields.Integer(required=True, description='ID of the location where asset is assigned'),
        'assigned_to': fields.String(required=True, description='Person or department assigned to the asset'),
        'assigned_date': fields.String(required=False, description='Date of assignment (YYYY-MM-DD)'),
        'return_date': fields.String(required=False, description='Expected return date of the asset (YYYY-MM-DD)')
    }
)

def serialize_date(date_obj):
    """Helper function to convert a date object to a string."""
    return date_obj.strftime('%Y-%m-%d') if date_obj else None

@assignment_ns.route('/')
class AssignmentListResource(Resource):
    
    #@jwt_required()
    @assignment_ns.expect(Assignment_model)
    def post(self):
        data = request.get_json()

        # Convert date strings to date objects
        if 'assigned_date' in data and data['assigned_date']:
            try:
                data['assigned_date'] = datetime.strptime(data['assigned_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid assigned_date format. Use YYYY-MM-DD'}), 400
        
        if 'return_date' in data and data['return_date']:
            try:
                data['return_date'] = datetime.strptime(data['return_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid return_date format. Use YYYY-MM-DD'}), 400

        required_fields = ['asset_id', 'location_id', 'assigned_to']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        new_assignment = Assignment(**data)

        try:
            db.session.add(new_assignment)
            db.session.commit()

            # Ensure new_assignment.to_dict() exists in the model
            return jsonify({
                'id': new_assignment.id,
                'asset_id': new_assignment.asset_id,
                'location_id': new_assignment.location_id,
                'assigned_to': new_assignment.assigned_to,
                'assigned_date': serialize_date(new_assignment.assigned_date),
                'return_date': serialize_date(new_assignment.return_date)
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    #@jwt_required()
    def get(self):
        assignments = Assignment.query.options(
            joinedload(Assignment.asset), 
            joinedload(Assignment.location)
        ).all()

        data = []
        for assignment in assignments:
            assignment_data = {
                'id': assignment.id,
                'asset_id': assignment.asset_id,
                'location_id': assignment.location_id,
                'assigned_to': assignment.assigned_to,
                'assigned_date': serialize_date(assignment.assigned_date),
                'return_date': serialize_date(assignment.return_date),
                'asset': assignment.asset.to_dict() if hasattr(assignment.asset, 'to_dict') else None,
                'location': assignment.location.to_dict() if hasattr(assignment.location, 'to_dict') else None
            }
            data.append(assignment_data)

        return jsonify(data)

@assignment_ns.route('/<int:assignment_id>')
class AssignmentResource(Resource):
    
    #@jwt_required()
    def get(self, assignment_id):
        assignment = Assignment.query.options(
            joinedload(Assignment.asset),
            joinedload(Assignment.location)
        ).get_or_404(assignment_id)

        return jsonify({
            'id': assignment.id,
            'asset_id': assignment.asset_id,
            'location_id': assignment.location_id,
            'assigned_to': assignment.assigned_to,
            'assigned_date': serialize_date(assignment.assigned_date),
            'return_date': serialize_date(assignment.return_date),
            'asset': assignment.asset.to_dict() if hasattr(assignment.asset, 'to_dict') else None,
            'location': assignment.location.to_dict() if hasattr(assignment.location, 'to_dict') else None
        })
    
    #@jwt_required()
    @assignment_ns.expect(Assignment_model)
    def put(self, assignment_id):
        assignment = Assignment.query.get_or_404(assignment_id)
        data = request.get_json()

        # Convert date strings to date objects
        if 'assigned_date' in data and data['assigned_date']:
            try:
                data['assigned_date'] = datetime.strptime(data['assigned_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid assigned_date format. Use YYYY-MM-DD'}), 400
        
        if 'return_date' in data and data['return_date']:
            try:
                data['return_date'] = datetime.strptime(data['return_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid return_date format. Use YYYY-MM-DD'}), 400

        for key, value in data.items():
            setattr(assignment, key, value)

        try:
            db.session.commit()
            return jsonify({
                'id': assignment.id,
                'asset_id': assignment.asset_id,
                'location_id': assignment.location_id,
                'assigned_to': assignment.assigned_to,
                'assigned_date': serialize_date(assignment.assigned_date),
                'return_date': serialize_date(assignment.return_date)
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    #@jwt_required()
    def delete(self, assignment_id):
        assignment = Assignment.query.get_or_404(assignment_id)

        try:
            db.session.delete(assignment)
            db.session.commit()
            return jsonify({'message': 'Assignment deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

# Register the namespace in your app
def register_routes(api):
    api.add_namespace(assignment_ns)
