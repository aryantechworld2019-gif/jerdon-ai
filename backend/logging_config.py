"""
Advanced logging configuration with structured logging.
Supports JSON logging for production and colored logs for development.
"""
import logging
import sys
from datetime import datetime
from pathlib import Path

try:
    import structlog
    from pythonjsonlogger import jsonlogger
    import colorlog
    ADVANCED_LOGGING_AVAILABLE = True
except ImportError:
    ADVANCED_LOGGING_AVAILABLE = False
    print("⚠️  Advanced logging dependencies not installed. Using basic logging.")

from config import ENVIRONMENT

# Create logs directory
LOGS_DIR = Path(__file__).parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

class CustomJSONFormatter(jsonlogger.JsonFormatter if ADVANCED_LOGGING_AVAILABLE else logging.Formatter):
    """Custom JSON formatter with additional fields"""

    def add_fields(self, log_record, record, message_dict):
        if not ADVANCED_LOGGING_AVAILABLE:
            return
        super().add_fields(log_record, record, message_dict)

        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        log_record['environment'] = ENVIRONMENT

        if hasattr(record, 'user_id'):
            log_record['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_record['request_id'] = record.request_id

def setup_logging():
    """Configure logging for the application"""

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    if ENVIRONMENT == "production" and ADVANCED_LOGGING_AVAILABLE:
        # Production: JSON logging
        file_handler = logging.FileHandler(
            LOGS_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(CustomJSONFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s'
        ))
        root_logger.addHandler(file_handler)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.INFO)
        stdout_handler.setFormatter(CustomJSONFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s'
        ))
        root_logger.addHandler(stdout_handler)

    else:
        # Development: Colored console logging
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        if ADVANCED_LOGGING_AVAILABLE:
            formatter = colorlog.ColoredFormatter(
                '%(log_color)s%(asctime)s [%(levelname)s] %(name)s:%(lineno)d%(reset)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                }
            )
        else:
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        # File logging in development
        file_handler = logging.FileHandler(LOGS_DIR / "development.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s'
        ))
        root_logger.addHandler(file_handler)

    # Reduce noise from third-party libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    # Configure structlog if available
    if ADVANCED_LOGGING_AVAILABLE:
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer() if ENVIRONMENT == "production"
                else structlog.dev.ConsoleRenderer(colors=True)
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

    logging.info(f"✅ Logging configured for {ENVIRONMENT} environment")

def get_logger(name: str):
    """Get a logger instance"""
    if ADVANCED_LOGGING_AVAILABLE:
        return structlog.get_logger(name)
    return logging.getLogger(name)

# Initialize logging
setup_logging()

__all__ = ['setup_logging', 'get_logger']
