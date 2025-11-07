"""
Request context middleware for tracking requests.
Adds request ID and user context to all logs.
"""
import uuid
import time
import logging
from contextvars import ContextVar
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

# Context variables
request_id_var: ContextVar[str] = ContextVar('request_id', default=None)
user_id_var: ContextVar[str] = ContextVar('user_id', default=None)

class RequestContextMiddleware(BaseHTTPMiddleware):
    """Middleware to add request context to logging"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        request_id_var.set(request_id)

        request.state.request_id = request_id
        start_time = time.time()

        logger.info(
            "Request started",
            extra={
                'request_id': request_id,
                'method': request.method,
                'path': request.url.path,
                'client_ip': request.client.host if request.client else None
            }
        )

        try:
            response = await call_next(request)
            duration = time.time() - start_time

            logger.info(
                "Request completed",
                extra={
                    'request_id': request_id,
                    'method': request.method,
                    'path': request.url.path,
                    'status_code': response.status_code,
                    'duration_ms': round(duration * 1000, 2)
                }
            )

            response.headers['X-Request-ID'] = request_id
            return response

        except Exception as e:
            duration = time.time() - start_time

            logger.error(
                "Request failed",
                extra={
                    'request_id': request_id,
                    'method': request.method,
                    'path': request.url.path,
                    'error': str(e),
                    'duration_ms': round(duration * 1000, 2)
                },
                exc_info=True
            )
            raise

def get_request_id() -> str:
    """Get current request ID from context"""
    return request_id_var.get()

def set_user_context(user_id: str):
    """Set user ID in context for logging"""
    user_id_var.set(user_id)

def get_user_id() -> str:
    """Get current user ID from context"""
    return user_id_var.get()

__all__ = [
    'RequestContextMiddleware',
    'get_request_id',
    'set_user_context',
    'get_user_id'
]
