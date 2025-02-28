# from flask import request, jsonify
# from flask_restx import Namespace, Resource, fields
# from exts import db
# from flask_jwt_extended import jwt_required
# from datetime import datetime

# # Create a namespace for assignments
# assignment_ns = Namespace('assignments', description='Asset assignment operations')

# Assignment_model = assignment_ns.model(
#     'Assignment',
#     {
#         'asset_id': fields.Integer(required=True, description='ID of the assigned asset'),
#         'location_id': fields.Integer(required=True, description='ID of the location where asset is assigned'),
#         'assigned_to': fields.String(required=True, description='Person or department assigned to the asset'),
#         'assigned_date': fields.String(required=False, description='Date of assignment (YYYY-MM-DD)'),
#         'return_date': fields.String(required=False, description='Expected return date of the asset (YYYY-MM-DD)')
#     }
# )

# def serialize_date(date_obj):
#     return date_obj.strftime('%Y-%m-%d') if date_obj else None

# @assignment_ns.route('/')
# class AssignmentListResource(Resource):
    
#     #@jwt_required()
#     @assignment_ns.expect(Assignment_model)
#     def post(self):
#         data = request.get_json()
        
#         assigned_date = data.get('assigned_date')
#         return_date = data.get('return_date')
        
#         query = """
#             INSERT INTO assignment (asset_id, location_id, assigned_to, assigned_date, return_date)
#             VALUES (%s, %s, %s, %s, %s) RETURNING id;
#         """
        
#         values = (
#             data['asset_id'], data['location_id'], data['assigned_to'],
#             assigned_date, return_date
#         )

#         try:
#             with db.engine.connect() as connection:
#                 result = connection.execute(query, values)
#                 assignment_id = result.fetchone()[0]
#                 return jsonify({'id': assignment_id, **data})
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500

#     #@jwt_required()
#     def get(self):
#         query = "SELECT * FROM assignment;"
        
#         with db.engine.connect() as connection:
#             result = connection.execute(query)
#             assignments = [dict(row) for row in result.mappings()]
#             return jsonify(assignments)

# @assignment_ns.route('/<int:assignment_id>')
# class AssignmentResource(Resource):
    
#     #@jwt_required()
#     def get(self, assignment_id):
#         query = "SELECT * FROM assignment WHERE id = %s;"
        
#         with db.engine.connect() as connection:
#             result = connection.execute(query, (assignment_id,))
#             assignment = result.mappings().first()
#             if not assignment:
#                 return jsonify({'error': 'Assignment not found'}), 404
#             return jsonify(dict(assignment))

#     #@jwt_required()
#     @assignment_ns.expect(Assignment_model)
#     def put(self, assignment_id):
#         data = request.get_json()
#         update_query = """
#             UPDATE assignment
#             SET asset_id = %s, location_id = %s, assigned_to = %s, assigned_date = %s, return_date = %s
#             WHERE id = %s;
#         """
        
#         values = (
#             data['asset_id'], data['location_id'], data['assigned_to'],
#             data.get('assigned_date'), data.get('return_date'), assignment_id
#         )
        
#         try:
#             with db.engine.connect() as connection:
#                 connection.execute(update_query, values)
#                 return jsonify({'message': 'Assignment updated successfully'})
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500

#     #@jwt_required()
#     def delete(self, assignment_id):
#         query = "DELETE FROM assignment WHERE id = %s;"
        
#         try:
#             with db.engine.connect() as connection:
#                 connection.execute(query, (assignment_id,))
#                 return jsonify({'message': 'Assignment deleted successfully'})
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500

# # Register the namespace in your app
# def register_routes(api):
#     api.add_namespace(assignment_ns)






from flask import request
from flask_restx import Namespace, Resource, fields
from exts import db
from sqlalchemy.sql import text  # 🔥 Import text for raw SQL execution
from flask_jwt_extended import jwt_required

# Create a namespace for assignments
assignment_ns = Namespace('assignments', description='Asset assignment operations')

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

@assignment_ns.route('/')
class AssignmentListResource(Resource):
    
    #@jwt_required()
    @assignment_ns.expect(Assignment_model)
    def post(self):
        data = request.get_json()

        query = text("""
            INSERT INTO assignment (asset_id, location_id, assigned_to, assigned_date, return_date)
            VALUES (:asset_id, :location_id, :assigned_to, :assigned_date, :return_date) RETURNING id;
        """)

        values = {
            'asset_id': data['asset_id'],
            'location_id': data['location_id'],
            'assigned_to': data['assigned_to'],
            'assigned_date': data.get('assigned_date'),
            'return_date': data.get('return_date')
        }

        try:
            with db.engine.connect() as connection:
                result = connection.execute(query, values)
                assignment_id = result.fetchone()[0]
                return {'id': assignment_id, **data}, 201
        except Exception as e:
            return {'error': str(e)}, 500

    #@jwt_required()
    def get(self):
        query = text("SELECT * FROM assignment;")
        
        with db.engine.connect() as connection:
            result = connection.execute(query)
            assignments = [dict(row) for row in result.mappings()]
            return assignments, 200

@assignment_ns.route('/<int:assignment_id>')
class AssignmentResource(Resource):
    
    #@jwt_required()
    def get(self, assignment_id):
        query = text("SELECT * FROM assignment WHERE id = :assignment_id;")
        
        with db.engine.connect() as connection:
            result = connection.execute(query, {'assignment_id': assignment_id})
            assignment = result.mappings().first()
            if not assignment:
                return {'error': 'Assignment not found'}, 404
            return dict(assignment), 200

    #@jwt_required()
    @assignment_ns.expect(Assignment_model)
    def put(self, assignment_id):
        data = request.get_json()
        update_query = text("""
            UPDATE assignment
            SET asset_id = :asset_id, location_id = :location_id, assigned_to = :assigned_to, 
                assigned_date = :assigned_date, return_date = :return_date
            WHERE id = :assignment_id;
        """)

        values = {
            'asset_id': data['asset_id'],
            'location_id': data['location_id'],
            'assigned_to': data['assigned_to'],
            'assigned_date': data.get('assigned_date'),
            'return_date': data.get('return_date'),
            'assignment_id': assignment_id
        }

        try:
            with db.engine.connect() as connection:
                connection.execute(update_query, values)
                return {'message': 'Assignment updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    #@jwt_required()
    def delete(self, assignment_id):
        query = text("DELETE FROM assignment WHERE id = :assignment_id;")
        
        try:
            with db.engine.connect() as connection:
                connection.execute(query, {'assignment_id': assignment_id})
                return {'message': 'Assignment deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

# Register the namespace in your app
def register_routes(api):
    api.add_namespace(assignment_ns)
