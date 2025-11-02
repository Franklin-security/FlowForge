"""
Main application entry point.

Integrates all FlowForge components: API, providers, database, background workers.
"""

import sys
import signal
import logging
from typing import Optional

from src.utils.logger import setup_logging, get_logger
from src.config import config
from src.database.db import get_db_manager

logger = get_logger(__name__)

# Global references for cleanup
_poller = None
_app = None


def setup_components():
    """
    Initialize all FlowForge components.
    
    Returns:
        tuple: (Flask app, Provider registry, Poller)
    """
    from src.api.routes import app
    from src.api.pipelines import get_registry
    from src.workers import PipelinePoller
    
    # Initialize database
    logger.info("Initializing database...")
    db = get_db_manager()
    db.init_db()
    logger.info("Database initialized")
    
    # Get provider registry
    registry = get_registry()
    
    # Initialize background poller (optional, can be started later)
    poller = PipelinePoller(registry, interval=30)
    
    return app, registry, poller


def start_background_services(registry, poller):
    """
    Start background services.
    
    Args:
        registry: Provider registry
        poller: Pipeline poller
    """
    global _poller
    
    # Load providers from keyring/config if available
    # This would typically be done via API or configuration
    logger.info("Background services ready (start via API or CLI)")
    
    _poller = poller
    # Don't auto-start poller - let it be started via API or explicitly


def cleanup():
    """Cleanup resources on shutdown."""
    global _poller
    
    logger.info("Shutting down FlowForge...")
    
    if _poller and _poller.running:
        _poller.stop()
        logger.info("Background poller stopped")
    
    logger.info("Shutdown complete")


def signal_handler(signum, frame):
    """Handle shutdown signals."""
    logger.info(f"Received signal {signum}, shutting down...")
    cleanup()
    sys.exit(0)


def main():
    """
    Main application function.
    
    Starts FlowForge with all integrated components:
    - Database initialization
    - API server
    - Background worker support
    - Provider registry
    """
    # Setup logging
    setup_logging(
        level=logging.DEBUG if config.DEBUG else logging.INFO,
        log_file='flowforge.log'
    )
    
    logger.info("=" * 60)
    logger.info(f"Starting {config.APP_NAME} v{config.APP_VERSION}")
    logger.info("=" * 60)
    
    try:
        # Initialize components
        app, registry, poller = setup_components()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Prepare background services (don't auto-start)
        start_background_services(registry, poller)
        
        # Start Flask server
        logger.info(f"Starting API server on {config.HOST}:{config.PORT}")
        logger.info(f"API endpoints available at: http://{config.HOST}:{config.PORT}/api/v1")
        logger.info(f"Health check: http://{config.HOST}:{config.PORT}/health")
        logger.info("")
        logger.info("FlowForge is ready!")
        logger.info("")
        logger.info("API Documentation:")
        logger.info("  GET  /api/v1/pipelines              - List all pipelines")
        logger.info("  GET  /api/v1/pipelines/providers    - List providers")
        logger.info("  POST /api/v1/providers               - Add provider")
        logger.info("  POST /api/v1/pipelines/<provider>/pipelines/<id>/trigger - Trigger pipeline")
        logger.info("")
        
        # Run Flask app
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
            use_reloader=False  # Disable reloader to avoid duplicate threads
        )
    
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        cleanup()
        return 0
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        cleanup()
        return 1


if __name__ == "__main__":
    sys.exit(main())

