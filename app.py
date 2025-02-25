# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_restx import Api
# from flask_migrate import Migrate  # Import Migrate

# from models import Asset, Location, Assignment  # Import the models after defining the app and db

# app = Flask(__name__)

# api=Api(app,doc='/docs')

# # Supabase Database Configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://p-admin:inventory2030@172.236.2.18:5432/db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)  # Initialize Migrate

# @app.route('/')
# def index():
#     return "Connected to PostgreSQL on Linode!"

# # Import routes from manage_fixed_asset_assignment after defining the app and db


# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    api = Api(app, doc='/docs')

    # Supabase Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://p-admin:inventory2030@172.236.2.18:5432/db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from models import Asset, Location, Assignment  # Import models here

    @app.route('/')
    def index():
        return "Connected to PostgreSQL on Linode!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)