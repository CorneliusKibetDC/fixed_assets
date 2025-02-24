from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Supabase Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://p-admin:inventory2030@localhost:5432/db?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Connected to Supabase PostgreSQL!"

if __name__ == '__main__':
    app.run(debug=True)

