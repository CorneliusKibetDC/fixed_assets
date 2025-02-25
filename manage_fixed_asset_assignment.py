# from flask import Blueprint, request, jsonify
# from app import db
# from models import Asset, Location, Assignment

# # Create a Blueprint for the asset assignment management
# assignment_bp = Blueprint('assignment', __name__)

# @assignment_bp.route('/assignments', methods=['POST'])
# def create_assignment():
#     data = request.get_json()
    
#     # Validate input
#     asset_id = data.get('asset_id')
#     location_id = data.get('location_id')
#     assigned_to = data.get('assigned_to')
#     assigned_date = data.get('assigned_date')
#     return_date = data.get('return_date')

#     if not all([asset_id, location_id, assigned_to]):
#         return jsonify({'error': 'Missing required fields'}), 400

#     # Create a new assignment
#     new_assignment = Assignment(
#         asset_id=asset_id,
#         location_id=location_id,
#         assigned_to=assigned_to,
#         assigned_date=assigned_date,
#         return_date=return_date
#     )

#     db.session.add(new_assignment)
#     db.session.commit()

#     return jsonify(new_assignment.to_dict()), 201

# @assignment_bp.route('/assignments/<int:assignment_id>', methods=['GET'])
# def get_assignment(assignment_id):
#     assignment = Assignment.query.get_or_404(assignment_id)
#     return jsonify(assignment.to_dict())

# @assignment_bp.route('/assignments/<int:assignment_id>', methods=['PUT'])
# def update_assignment(assignment_id):
#     assignment = Assignment.query.get_or_404(assignment_id)
#     data = request.get_json()

#     # Update fields from the request
#     if 'asset_id' in data:
#         assignment.asset_id = data['asset_id']
#     if 'location_id' in data:
#         assignment.location_id = data['location_id']
#     if 'assigned_to' in data:
#         assignment.assigned_to = data['assigned_to']
#     if 'assigned_date' in data:
#         assignment.assigned_date = data['assigned_date']
#     if 'return_date' in data:
#         assignment.return_date = data['return_date']

#     db.session.commit()
#     return jsonify(assignment.to_dict())

# @assignment_bp.route('/assignments/<int:assignment_id>', methods=['DELETE'])
# def delete_assignment(assignment_id):
#     assignment = Assignment.query.get_or_404(assignment_id)
#     db.session.delete(assignment)
#     db.session.commit()
#     return jsonify({'message': 'Assignment deleted successfully'}), 204

# @assignment_bp.route('/assignments', methods=['GET'])
# def get_assignments():
#     assignments = Assignment.query.all()
#     return jsonify([assignment.to_dict() for assignment in assignments])

# # Register the blueprint in your app
# def register_routes(app):
#     app.register_blueprint(assignment_bp)










### manage_fixed_asset_assignment.py

# from flask import request, jsonify
# from flask_restx import Namespace, Resource
# from app import db
# from models import Asset, Location, Assignment
# from flask_jwt_extended import jwt_required

# # Create a namespace for assignments
# assignment_ns = Namespace('assignments', description='Asset assignment operations')

# @assignment_ns.route('/')
# class AssignmentList(Resource):
#     #@jwt_required()
#     def post(self):
#         data = request.get_json()
        
#         # Validate input
#         asset_id = data.get('asset_id')
#         location_id = data.get('location_id')
#         assigned_to = data.get('assigned_to')
#         assigned_date = data.get('assigned_date')
#         return_date = data.get('return_date')

#         if not all([asset_id, location_id, assigned_to]):
#             return jsonify({'error': 'Missing required fields'}), 400

#         # Create a new assignment
#         new_assignment = Assignment(
#             asset_id=asset_id,
#             location_id=location_id,
#             assigned_to=assigned_to,
#             assigned_date=assigned_date,
#             return_date=return_date
#         )

#         db.session.add(new_assignment)
#         db.session.commit()

#         return jsonify(new_assignment.to_dict()), 201

#     #@jwt_required()
#     def get(self):
#         assignments = Assignment.query.all()
#         return jsonify([assignment.to_dict() for assignment in assignments]), 200

# @assignment_ns.route('/<int:assignment_id>')
# class AssignmentResource(Resource):
#     #@jwt_required()
#     def get(self, assignment_id):
#         assignment = Assignment.query.get_or_404(assignment_id)
#         return jsonify(assignment.to_dict()), 200

#     #@jwt_required()
#     def put(self, assignment_id):
#         assignment = Assignment.query.get_or_404(assignment_id)
#         data = request.get_json()

#         # Update fields from the request
#         if 'asset_id' in data:
#             assignment.asset_id = data['asset_id']
#         if 'location_id' in data:
#             assignment.location_id = data['location_id']
#         if 'assigned_to' in data:
#             assignment.assigned_to = data['assigned_to']
#         if 'assigned_date' in data:
#             assignment.assigned_date = data['assigned_date']
#         if 'return_date' in data:
#             assignment.return_date = data['return_date']

#         db.session.commit()
#         return jsonify(assignment.to_dict()), 200

#     #@jwt_required()
#     def delete(self, assignment_id):
#         assignment = Assignment.query.get_or_404(assignment_id)
#         db.session.delete(assignment)
#         db.session.commit()
#         return jsonify({'message': 'Assignment deleted successfully'}), 204

# # Register the namespace in your app
# def register_routes(api):
#     api.add_namespace(assignment_ns)












from flask import request, jsonify
from flask_restx import Namespace, Resource
from app import db
from models import Asset, Location, Assignment
from flask_jwt_extended import jwt_required

# Create a namespace for assignments
assignment_ns = Namespace('assignments', description='Asset assignment operations')

@assignment_ns.route('/')
class AssignmentList(Resource):
    #@jwt_required()
    def post(self):
        data = request.get_json()
        
        # Validate input
        asset_id = data.get('asset_id')
        location_id = data.get('location_id')
        assigned_to = data.get('assigned_to')
        assigned_date = data.get('assigned_date')
        return_date = data.get('return_date')

        if not all([asset_id, location_id, assigned_to]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Create a new assignment
        new_assignment = Assignment(
            asset_id=asset_id,
            location_id=location_id,
            assigned_to=assigned_to,
            assigned_date=assigned_date,
            return_date=return_date
        )

        try:
            db.session.add(new_assignment)
            db.session.commit()
            return jsonify(new_assignment.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    #@jwt_required()
    def get(self):
        assignments = Assignment.query.all()
        return jsonify([assignment.to_dict() for assignment in assignments]), 200

@assignment_ns.route('/<int:assignment_id>')
class AssignmentResource(Resource):
    #@jwt_required()
    def get(self, assignment_id):
        assignment = Assignment.query.get_or_404(assignment_id)
        return jsonify(assignment.to_dict()), 200

    #@jwt_required()
    def put(self, assignment_id):
        assignment = Assignment.query.get_or_404(assignment_id)
        data = request.get_json()

        # Update fields from the request
        if 'asset_id' in data:
            assignment.asset_id = data['asset_id']
        if 'location_id' in data:
            assignment.location_id = data['location_id']
        if 'assigned_to' in data:
            assignment.assigned_to = data['assigned_to']
        if 'assigned_date' in data:
            assignment.assigned_date = data['assigned_date']
        if 'return_date' in data:
            assignment.return_date = data['return_date']

        try:
            db.session.commit()
            return jsonify(assignment.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    #@jwt_required()
    def delete(self, assignment_id):
        assignment = Assignment.query.get_or_404(assignment_id)
        try:
            db.session.delete(assignment)
            db.session.commit()
            return jsonify({'message': 'Assignment deleted successfully'}), 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

# Register the namespace in your app
def register_routes(api):
    api.add_namespace(assignment_ns)
