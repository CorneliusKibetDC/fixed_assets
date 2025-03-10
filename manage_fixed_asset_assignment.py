
from flask import request
from flask_restx import Namespace, Resource, fields
from exts import db
from sqlalchemy.sql import text
from flask_jwt_extended import jwt_required
from datetime import date

# Create a namespace for assignments
assignment_ns = Namespace('assignments', description='Asset assignment operations')

Assignment_model = assignment_ns.model(
    'Assignment',
    {
        'asset_id': fields.Integer(required=True, description='ID of the assigned asset'),
        'location_id': fields.Integer(required=False, description='ID of the location where asset is assigned'),
        'assigned_to': fields.String(required=False, description='Person assigned to the asset'),
        'assigned_date': fields.String(required=False, description='Date of assignment (YYYY-MM-DD)'),
        'return_date': fields.String(required=False, description='Expected return date of the asset (YYYY-MM-DD)')
    }
)

@assignment_ns.route('/')
class AssignmentListResource(Resource):
    @assignment_ns.expect(Assignment_model)
    def post(self):
        data = request.get_json()

        # Ensure at least one of location_id or assigned_to is provided
        if not data.get('location_id') and not data.get('assigned_to'):
            return {'error': 'Either location_id or assigned_to must be provided'}, 400

        check_asset_query = text("SELECT status FROM asset WHERE id = :asset_id;")
        insert_query = text("""
            INSERT INTO assignment (asset_id, location_id, assigned_to, assigned_date, return_date)
            VALUES (:asset_id, :location_id, :assigned_to, :assigned_date, :return_date) RETURNING id;
        """)
        update_asset_status_query = text("""
            UPDATE asset SET status = 'assigned' WHERE id = :asset_id;
        """)
        update_asset_location_query = text("""
            UPDATE asset SET location_id = :location_id WHERE id = :asset_id;
        """)

        values = {
            'asset_id': data['asset_id'],
            'location_id': data.get('location_id'),
            'assigned_to': data.get('assigned_to'),
            'assigned_date': data.get('assigned_date'),
            'return_date': data.get('return_date')
        }

        try:
            with db.engine.begin() as connection:
                asset_status = connection.execute(check_asset_query, {'asset_id': data['asset_id']}).scalar()
                if asset_status == 'assigned':
                    return {'error': 'Asset is already assigned'}, 400

                result = connection.execute(insert_query, values)
                assignment_id = result.fetchone()[0]

                connection.execute(update_asset_status_query, {'asset_id': data['asset_id']})
                if data.get('location_id'):
                    connection.execute(update_asset_location_query, values)

                return {'id': assignment_id, **data}, 201
        except Exception as e:
            return {'error': str(e)}, 500

    def get(self):
        query = text("SELECT * FROM assignment;")

        with db.engine.connect() as connection:
            result = connection.execute(query)
            assignments = []
            for row in result.mappings():
                assignment = dict(row)
                if isinstance(assignment.get('assigned_date'), date):
                    assignment['assigned_date'] = assignment['assigned_date'].isoformat()
                if isinstance(assignment.get('return_date'), date):
                    assignment['return_date'] = assignment['return_date'].isoformat()
                assignments.append(assignment)

            return assignments, 200

@assignment_ns.route('/<int:assignment_id>')
class AssignmentResource(Resource):
    def get(self, assignment_id):
        query = text("SELECT * FROM assignment WHERE id = :assignment_id;")

        with db.engine.connect() as connection:
            result = connection.execute(query, {'assignment_id': assignment_id})
            assignment = result.mappings().first()
            if not assignment:
                return {'error': 'Assignment not found'}, 404

            assignment = dict(assignment)
            if isinstance(assignment.get('assigned_date'), date):
                assignment['assigned_date'] = assignment['assigned_date'].isoformat()
            if isinstance(assignment.get('return_date'), date):
                assignment['return_date'] = assignment['return_date'].isoformat()

            return assignment, 200

    @assignment_ns.expect(Assignment_model)
    def put(self, assignment_id):
        data = request.get_json()

        # Ensure at least one of location_id or assigned_to is provided
        if not data.get('location_id') and not data.get('assigned_to'):
            return {'error': 'Either location_id or assigned_to must be provided'}, 400

        update_query = text("""
            UPDATE assignment
            SET asset_id = :asset_id, location_id = :location_id, assigned_to = :assigned_to, 
                assigned_date = :assigned_date, return_date = :return_date
            WHERE id = :assignment_id;
        """)

        update_asset_location_query = text("""
            UPDATE asset SET location_id = :location_id WHERE id = :asset_id;
        """)

        values = {
            'asset_id': data['asset_id'],
            'location_id': data.get('location_id'),
            'assigned_to': data.get('assigned_to'),
            'assigned_date': data.get('assigned_date'),
            'return_date': data.get('return_date'),
            'assignment_id': assignment_id
        }

        try:
            with db.engine.begin() as connection:
                connection.execute(update_query, values)
                if data.get('location_id'):
                    connection.execute(update_asset_location_query, values)
                return {'message': 'Assignment updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def delete(self, assignment_id):
        query = text("DELETE FROM assignment WHERE id = :assignment_id;")
        
        try:
            with db.engine.connect() as connection:
                connection.execute(query, {'assignment_id': assignment_id})
                connection.commit()
                return {'message': 'Assignment deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500
@assignment_ns.route('/<int:assignment_id>/return')
class ReturnAssignmentResource(Resource):
    def patch(self, assignment_id):
        return_date = date.today().isoformat()

        get_assignment_query = text("SELECT asset_id FROM assignment WHERE id = :assignment_id;")
        update_assignment_query = text("""
            UPDATE assignment 
            SET return_date = :return_date 
            WHERE id = :assignment_id;
        """)
        update_asset_status_query = text("""
            UPDATE asset 
            SET status = 'available', assigned_to = NULL 
            WHERE id = :asset_id;
        """)
        delete_assignment_query = text("DELETE FROM assignment WHERE id = :assignment_id;")

        try:
            with db.engine.begin() as connection:
                result = connection.execute(get_assignment_query, {'assignment_id': assignment_id})
                assignment = result.mappings().first()
                if not assignment:
                    return {'error': 'Assignment not found'}, 404

                asset_id = assignment['asset_id']
                connection.execute(update_assignment_query, {'return_date': return_date, 'assignment_id': assignment_id})
                connection.execute(update_asset_status_query, {'asset_id': asset_id})
                connection.execute(delete_assignment_query, {'assignment_id': assignment_id})

                return {
                    'message': 'Asset returned successfully',
                    'return_date': return_date
                }, 200
        except Exception as e:
            return {'error': str(e)}, 500
        



# Register the namespace in your app
def register_routes(api):
    api.add_namespace(assignment_ns)










