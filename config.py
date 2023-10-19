import os

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your_secret_key'  # Change this to a random and secure value

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'sqlite:///development_database.db'
    SECRET_KEY = 'development_secret_key'

class ProductionConfig(Config):
    DATABASE_URI = os.getenv('DATABASE_URL')  # Example: 'postgresql://user:password@localhost/dbname'
    SECRET_KEY = os.getenv('SECRET_KEY')  # Example: 'super_secret_production_key'

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = 'sqlite:///test_database.db'
    SECRET_KEY = 'testing_secret_key'