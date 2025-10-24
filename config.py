import os

class Config:
    """Configuration class for SmartML Dashboard"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'smartml-secret-key-2025'
    DEBUG = True
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'csv'}
    
    # Sample datasets folder
    SAMPLE_DATASETS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_datasets')
    
    # ML settings
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    
    # Visualization settings
    PLOT_STYLE = 'seaborn-v0_8-darkgrid'
    FIGURE_SIZE = (10, 6)
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        # Create upload folder if it doesn't exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.SAMPLE_DATASETS_FOLDER, exist_ok=True)
