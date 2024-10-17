# libs/logger.py
import logging
import logging.config
from models import Settings

def setup_logging():
    """Set up logging configuration based on the LOG_LEVEL and LOG_FILE_LEVEL environment variables."""
    settings = Settings()  # Initialize Settings to access LOG_LEVEL and LOG_FILE_LEVEL

    # Retrieve the log level for the console handler from settings, default to 'INFO' if not set or invalid
    log_level_str = settings.LOG_LEVEL.upper() if hasattr(settings, 'LOG_LEVEL') else 'INFO'
    # Retrieve the log level for the file handler from settings, default to 'INFO' if not set or invalid
    log_file_level_str = settings.LOG_FILE_LEVEL.upper() if hasattr(settings, 'LOG_FILE_LEVEL') else 'INFO'

    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    # Validate and set the console log level
    if log_level_str not in valid_levels:
        log_level_str = 'INFO'  # Fallback to INFO if invalid log level is provided

    # Validate and set the file log level
    if log_file_level_str not in valid_levels:
        log_file_level_str = 'INFO'  # Fallback to INFO if invalid log level is provided

    config = {
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'standard': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
            },
            'detailed': {
                'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d]: %(message)s'
            },
        },

        'handlers': {
            'console': {
                'level': log_level_str,  # Use the log level from LOG_LEVEL
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
            'file': {
                'level': log_file_level_str,  # Use the log level from LOG_FILE_LEVEL
                'class': 'logging.FileHandler',
                'formatter': 'detailed',
                'filename': 'app.log',  # Make this path configurable if needed
                'mode': 'a',
            },
        },

        'loggers': {
            # Root logger configuration
            '': {
                'handlers': ['console', 'file'],
                'level': log_level_str,  # Use the log level from LOG_LEVEL
                'propagate': True
            },
            # Example of a specific logger (optional)
            # 'my_module': {
            #     'handlers': ['console'],
            #     'level': 'DEBUG',
            #     'propagate': False
            # },
        }
    }

    # Apply the logging configuration
    logging.config.dictConfig(config)

    # Optional: Set the root logger's level explicitly
    logging.getLogger().setLevel(log_level_str)
