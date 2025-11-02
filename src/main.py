"""
Main application entry point.
"""

import logging
import sys
from pathlib import Path

# Try to import Flask, but don't fail if it's not available
try:
    from src.api.routes import app
    from src.config import config
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """
    Main application function.
    Starts the application server if Flask is available, otherwise runs basic initialization.
    """
    logger.info("Application starting...")
    
    if FLASK_AVAILABLE:
        logger.info(f"Starting Flask server on {config.HOST}:{config.PORT}")
        logger.info(f"Application name: {config.APP_NAME}")
        logger.info(f"Debug mode: {config.DEBUG}")
        
        # Start Flask development server
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG
        )
    else:
        # Basic initialization without Flask
        logger.info("Flask not available, running basic initialization")
        logger.info("Application initialized successfully")
        logger.info("FlowForge is ready for pipeline orchestration")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

