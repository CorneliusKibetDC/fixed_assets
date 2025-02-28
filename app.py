from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource
from flask_migrate import Migrate
from flask_cors import CORS
import os
from exts import db
from models import create_tables
from fixed_asset import asset_ns
from config import ProdConfig
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(ProdConfig)
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # ✅ FIX: Ensure tables exist inside app context
    with app.app_context():
        create_tables()

    # Register API and Blueprint
    api = Api(app, doc='/docs', title='Asset Management API', description='API for managing assets')
    api.add_namespace(asset_ns)

    # Register routes
    from manage_fixed_asset_assignment import register_routes as register_assignment_routes
    from manage_fixed_asset_locations import register_routes as register_location_routes
    from fixed_asset import register_routes as register_filter_routes
    from fixed_asset import register_routes as register_asset_routes

    register_assignment_routes(api)
    register_location_routes(api)
    register_filter_routes(api)
    register_asset_routes(api)

    # Test Route
    @app.route('/ping', methods=['GET'])
    def ping():
        return {"message": "pong"}, 200

    # Root route
    @api.route('/')
    class Index(Resource):
        def get(self):
            return {"message": "Connected to PostgreSQL on Linode!"}

    return app

# Run the application
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5050, host="0.0.0.0")
