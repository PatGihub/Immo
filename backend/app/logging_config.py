import logging
import logging.handlers
from pathlib import Path
from app.config import settings

# Create logs directory
logs_dir = Path(__file__).parent.parent / "logs"
logs_dir.mkdir(exist_ok=True)

# Configure logging
def setup_logging():
    """Setup logging configuration"""
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Toujours DEBUG pour plus de détails
    
    # Log format avec plus d'informations
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Afficher tous les logs en console
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)
    
    # File handler - rotating file
    file_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "app.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)
    
    # API requests handler
    api_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "api_requests.log",
        maxBytes=10*1024*1024,
        backupCount=5
    )
    api_handler.setLevel(logging.DEBUG)  # DEBUG pour API aussi
    api_handler.setFormatter(log_format)
    
    # Get API logger
    api_logger = logging.getLogger("api")
    api_logger.setLevel(logging.DEBUG)
    api_logger.addHandler(api_handler)
    
    # Auth logger
    auth_logger = logging.getLogger("auth")
    auth_logger.setLevel(logging.DEBUG)
    auth_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "auth.log",
        maxBytes=10*1024*1024,
        backupCount=5
    )
    auth_handler.setLevel(logging.DEBUG)
    auth_handler.setFormatter(log_format)
    auth_logger.addHandler(auth_handler)
    
    return root_logger, api_logger, auth_logger

# Initialize loggers
logger, api_logger, auth_logger = setup_logging()
