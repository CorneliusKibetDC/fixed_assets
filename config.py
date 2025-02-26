import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    DB_USER = os.getenv('DB_USER')  
    DB_PASSWORD = os.getenv('DB_PASSWORD')  
    DB_HOST = os.getenv('DB_HOST', 'localhost') 
    DB_PORT = os.getenv('DB_PORT', '5432') 
    DB_NAME = os.getenv('DB_NAME')  
    
    
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    
    
