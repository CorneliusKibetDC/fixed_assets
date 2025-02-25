from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

app = Flask(__name__)

api=Api(app,doc='/docs')

# Supabase Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://p-admin:inventory2030@172.236.2.18:5432/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Connected to PostgreSQL on Linode!"

# Import routes from manage_fixed_asset_assignment after defining the app and db


if __name__ == '__main__':
    app.run(debug=True)