# # from flask import Flask
# # from flask_sqlalchemy import SQLAlchemy
# # from flask_restx import Api
# # from flask_migrate import Migrate  # Import Migrate

# # from models import Asset, Location, Assignment  # Import the models after defining the app and db

# # app = Flask(__name__)

# # api=Api(app,doc='/docs')

# # # Supabase Database Configuration
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://p-admin:inventory2030@172.236.2.18:5432/db'
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # db = SQLAlchemy(app)
# # migrate = Migrate(app, db)  # Initialize Migrate

# # @app.route('/')
# # def index():
# #     return "Connected to PostgreSQL on Linode!"

# # # Import routes from manage_fixed_asset_assignment after defining the app and db


# # if __name__ == '__main__':
# #     app.run(debug=True)






# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_restx import Api
# from flask_migrate import Migrate
# #from manage_fixed_asset_assignment import register_routes as register_assignment_routes
# #from manage_fixed_asset_locations import register_routes as register_location_routes  # Import the routes

# db = SQLAlchemy()
# migrate = Migrate()

# def create_app():
#     app = Flask(__name__)

#     api = Api(app, doc='/docs')

#     # Supabase Database Configuration
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://p-admin:inventory2030@172.236.2.18:5432/db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     db.init_app(app)
#     migrate.init_app(app, db)

#     with app.app_context():
#         from models import Asset, Location, Assignment  # Import models here
#         from manage_fixed_asset_assignment import register_routes as register_assignment_routes
#         from manage_fixed_asset_locations import register_routes as register_location_routes  # Import the routes

#         register_assignment_routes(app)  # Register the assignment routes
#         register_location_routes(app)     # Register the location routes

#     @app.route('/')
#     def index():
#         return "Connected to PostgreSQL on Linode!"

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)







# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_restx import Api
# from flask_migrate import Migrate
# import os  # Import os for environment variables

# db = SQLAlchemy()
# migrate = Migrate()

# def create_app():
#     app = Flask(__name__)

#     # Initialize the Api instance
#     api = Api(app, doc='/docs')

#     # Supabase Database Configuration (use environment variables for sensitive data)
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql+psycopg2://p-admin:inventory2030@172.236.2.18:5432/db')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     db.init_app(app)
#     migrate.init_app(app, db)

#     with app.app_context():
#         from models import Asset, Location, Assignment  # Import models here
#         from manage_fixed_asset_assignment import register_routes as register_assignment_routes
#         from manage_fixed_asset_locations import register_routes as register_location_routes
#         from filter_assets import register_routes as register_filter_routes
#         from delete_fixed_asset import register_routes as register_delete_routes

#         # Register the routes with the Api instance
#         register_assignment_routes(api)
#         register_location_routes(api)
#         register_filter_routes(api)
#         register_delete_routes(api)

#     @api.route('/')  # Use the api instance for the root route
#     def index():
#         return "Connected to PostgreSQL on Linode!"

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)







# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_restx import Api, Resource  # Import Resource
# from flask_migrate import Migrate
# import os

# db = SQLAlchemy()
# migrate = Migrate()
# api = Api(doc='/docs')

# def create_app():
#     app = Flask(__name__)

#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql+psycopg2://p-admin:inventory2030@172.236.2.18:5432/db')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     db.init_app(app)
#     migrate.init_app(app, db)
#     api.init_app(app)

#     with app.app_context():
#         from models import Asset, Location, Assignment
#         from manage_fixed_asset_assignment import register_routes as register_assignment_routes
#         from manage_fixed_asset_locations import register_routes as register_location_routes
#         from filter_assets import register_routes as register_filter_routes
#         from delete_fixed_asset import register_routes as register_delete_routes
#         from add_fixed_asset import register_routes as register_add_asset_routes

#         # Register the routes
#         register_assignment_routes(api)
#         register_location_routes(api)
#         register_filter_routes(api)
#         register_delete_routes(api)
#         register_add_asset_routes(api)

#     # ✅ Use class-based Resource for the root route
#     @api.route('/')
#     class Index(Resource):
#         def get(self):
#             return {"message": "Connected to PostgreSQL on Linode!"}

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)








# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_restx import Api, Resource
# from flask_migrate import Migrate
# import os

# # Initialize globally
# db = SQLAlchemy()
# migrate = Migrate()

# def create_app():
#     app = Flask(__name__)

#     # Database configuration
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql+psycopg2://p-admin:inventory2030@172.236.2.18:5432/db')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     # Initialize extensions
#     db.init_app(app)
#     migrate.init_app(app, db)
#     api = Api(app, doc='/docs')

#     # Import models to register them with SQLAlchemy
#     from models import Asset, Location, Assignment

#     # Register blueprints/routes
#     from manage_fixed_asset_assignment import register_routes as register_assignment_routes
#     from manage_fixed_asset_locations import register_routes as register_location_routes
#     from filter_assets import register_routes as register_filter_routes
#     from delete_fixed_asset import register_routes as register_delete_routes
#     from add_fixed_asset import register_routes as register_add_asset_routes

#     register_assignment_routes(api)
#     register_location_routes(api)
#     register_filter_routes(api)
#     register_delete_routes(api)
#     register_add_asset_routes(api)
    
#     @app.route('/ping', methods=['GET'])
#     def ping():
#         return {"message": "pong"}, 200


#     # Root route
#     @api.route('/')
#     class Index(Resource):
#         def get(self):
#             return {"message": "Connected to PostgreSQL on Linode!"}

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)









from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource
from flask_migrate import Migrate
import os

# Initialize globally
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql+psycopg2://p-admin:inventory2030@172.236.2.18:5432/db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    #api = Api(app, doc='/docs')
    api = Api(app, doc='/docs', title='Asset Management API', description='API for managing assets')

    # Import models after initializing db to avoid circular imports
    from models import Asset, Location, Assignment

    # Register blueprints/routes
    from manage_fixed_asset_assignment import register_routes as register_assignment_routes
    from manage_fixed_asset_locations import register_routes as register_location_routes
    from filter_assets import register_routes as register_filter_routes
    from delete_fixed_asset import register_routes as register_delete_routes
    from add_fixed_asset import register_routes as register_add_asset_routes

    register_assignment_routes(api)
    register_location_routes(api)
    register_filter_routes(api)
    register_delete_routes(api)
    register_add_asset_routes(api)

    @app.route('/ping', methods=['GET'])
    def ping():
        return {"message": "pong"}, 200

    # Root route
    @api.route('/')
    class Index(Resource):
        def get(self):
            return {"message": "Connected to PostgreSQL on Linode!"}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
