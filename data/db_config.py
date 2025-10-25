"""
Database configuration for Oasis
Supports both SQLite (development) and PostgreSQL (production)
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConfig:
    """Database configuration class"""
    
    @staticmethod
    def get_db_url():
        """Get database URL based on environment"""
        # Check if we're using PostgreSQL
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            return database_url
        
        # Check if we're using individual PostgreSQL config
        db_host = os.getenv('DB_HOST')
        db_name = os.getenv('DB_NAME')
        if db_host and db_name:
            db_user = os.getenv('DB_USER', 'oasis_user')
            db_password = os.getenv('DB_PASSWORD', 'oasis_password')
            db_port = os.getenv('DB_PORT', '5432')
            return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        # Default to SQLite
        db_path = os.getenv('DB_PATH', 'data/market_data.db')
        return f"sqlite:///{db_path}"
    
    @staticmethod
    def is_postgresql():
        """Check if we're using PostgreSQL"""
        db_url = DatabaseConfig.get_db_url()
        return db_url.startswith('postgresql')
    
    @staticmethod
    def is_sqlite():
        """Check if we're using SQLite"""
        db_url = DatabaseConfig.get_db_url()
        return db_url.startswith('sqlite')