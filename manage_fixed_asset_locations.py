from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from exts import db  # Import the database engine

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
    @location_ns.expect(Location_model)
    def post(self):
        data = request.get_json()
        query = """
        INSERT INTO location (name, description) 
        VALUES (:name, :description) RETURNING id;
        """
        
        with db.engine.connect() as connection:
            result = connection.execute(db.text(query), data)
            location_id = result.scalar()
            connection.commit()

        return {"id": location_id, **data}, 201

    def get(self):
        query = """
        SELECT l.id, l.name, l.description, 
               COALESCE(json_agg(a) FILTER (WHERE a.id IS NOT NULL), '[]') AS assets
        FROM location l
        LEFT JOIN assignment a ON l.id = a.location_id
        GROUP BY l.id;
        """
        
        with db.engine.connect() as connection:
            result = connection.execute(db.text(query))
            locations = [dict(row._mapping) for row in result]
        
        return locations, 200

@location_ns.route('/<int:location_id>')
class LocationResource(Resource):
    def get(self, location_id):
        query = """
        SELECT l.id, l.name, l.description, 
               COALESCE(json_agg(a) FILTER (WHERE a.id IS NOT NULL), '[]') AS assets
        FROM location l
        LEFT JOIN assignment a ON l.id = a.location_id
        WHERE l.id = :location_id
        GROUP BY l.id;
        """
        
        with db.engine.connect() as connection:
            result = connection.execute(db.text(query), {'location_id': location_id})
            location = result.fetchone()
        
        if not location:
            return {'error': 'Location not found'}, 404
        
        return dict(location._mapping), 200

    @location_ns.expect(Location_model)
    def put(self, location_id):
        data = request.get_json()
        query = """
        UPDATE location SET name = :name, description = :description WHERE id = :location_id;
        """
        
        with db.engine.connect() as connection:
            result = connection.execute(db.text(query), {**data, 'location_id': location_id})
            connection.commit()

        return {"id": location_id, **data}, 200

    def delete(self, location_id):
        query = "DELETE FROM location WHERE id = :location_id;"
        
        with db.engine.connect() as connection:
            connection.execute(db.text(query), {'location_id': location_id})
            connection.commit()
        
        return '', 204  # No content for 204 response

# Register the namespace in your app
def register_routes(api):
    api.add_namespace(location_ns)
