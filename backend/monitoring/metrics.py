"""
Application metrics using Prometheus.
Tracks API performance, database queries, cache hits, and business metrics.
"""
import time
import logging
from functools import wraps
from typing import Callable

try:
    from prometheus_client import (
        Counter,
        Histogram,
        Gauge,
        Info,
        CollectorRegistry,
        generate_latest,
        CONTENT_TYPE_LATEST
    )
    import psutil
    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False
    print("⚠️  Prometheus dependencies not installed. Metrics disabled.")

from config import APP_VERSION, ENVIRONMENT

logger = logging.getLogger(__name__)

if METRICS_AVAILABLE:
    # Create custom registry
    registry = CollectorRegistry()

    # API Metrics
    api_requests_total = Counter(
        'api_requests_total',
        'Total API requests',
        ['method', 'endpoint', 'status'],
        registry=registry
    )

    api_request_duration = Histogram(
        'api_request_duration_seconds',
        'API request duration in seconds',
        ['method', 'endpoint'],
        registry=registry,
        buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
    )

    api_requests_active = Gauge(
        'api_requests_active',
        'Number of active API requests',
        registry=registry
    )

    # Business Metrics
    chat_requests_total = Counter(
        'chat_requests_total',
        'Total chat requests',
        ['user_plan', 'has_context'],
        registry=registry
    )

    file_uploads_total = Counter(
        'file_uploads_total',
        'Total file uploads',
        ['user_plan', 'file_type'],
        registry=registry
    )

    user_registrations_total = Counter(
        'user_registrations_total',
        'Total user registrations',
        ['plan'],
        registry=registry
    )

    plan_upgrades_total = Counter(
        'plan_upgrades_total',
        'Total plan upgrades',
        ['from_plan', 'to_plan'],
        registry=registry
    )

    # System Metrics
    system_info = Info(
        'app_info',
        'Application information',
        registry=registry
    )
    system_info.info({
        'version': APP_VERSION,
        'environment': ENVIRONMENT
    })

    system_cpu_usage = Gauge(
        'system_cpu_usage_percent',
        'System CPU usage percentage',
        registry=registry
    )

    system_memory_usage = Gauge(
        'system_memory_usage_bytes',
        'System memory usage in bytes',
        registry=registry
    )

    # Error Metrics
    errors_total = Counter(
        'errors_total',
        'Total errors',
        ['type', 'endpoint'],
        registry=registry
    )

    def track_api_request(endpoint: str):
        """Decorator to track API request metrics"""
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                api_requests_active.inc()
                start_time = time.time()
                status_code = 200

                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    status_code = getattr(e, 'status_code', 500)
                    errors_total.labels(
                        type=type(e).__name__,
                        endpoint=endpoint
                    ).inc()
                    raise
                finally:
                    duration = time.time() - start_time
                    method = "unknown"
                    for arg in args:
                        if hasattr(arg, 'method'):
                            method = arg.method
                            break

                    api_requests_total.labels(
                        method=method,
                        endpoint=endpoint,
                        status=str(status_code)
                    ).inc()

                    api_request_duration.labels(
                        method=method,
                        endpoint=endpoint
                    ).observe(duration)

                    api_requests_active.dec()

            return wrapper
        return decorator

    def update_system_metrics():
        """Update system resource metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            system_cpu_usage.set(cpu_percent)

            memory = psutil.virtual_memory()
            system_memory_usage.set(memory.used)
        except Exception as e:
            logger.error(f"Error updating system metrics: {e}")

    def get_metrics() -> bytes:
        """Get current metrics in Prometheus format"""
        update_system_metrics()
        return generate_latest(registry)

    def get_metrics_content_type() -> str:
        """Get metrics content type"""
        return CONTENT_TYPE_LATEST

else:
    # Dummy implementations when metrics not available
    class DummyMetric:
        def labels(self, **kwargs):
            return self
        def inc(self, amount=1):
            pass
        def dec(self, amount=1):
            pass
        def set(self, value):
            pass
        def observe(self, value):
            pass
        def info(self, data):
            pass

    api_requests_total = DummyMetric()
    api_request_duration = DummyMetric()
    chat_requests_total = DummyMetric()
    file_uploads_total = DummyMetric()
    user_registrations_total = DummyMetric()
    plan_upgrades_total = DummyMetric()
    errors_total = DummyMetric()

    def track_api_request(endpoint: str):
        def decorator(func: Callable):
            return func
        return decorator

    def get_metrics() -> bytes:
        return b"Metrics not available"

    def get_metrics_content_type() -> str:
        return "text/plain"

__all__ = [
    'api_requests_total',
    'api_request_duration',
    'chat_requests_total',
    'file_uploads_total',
    'user_registrations_total',
    'plan_upgrades_total',
    'errors_total',
    'track_api_request',
    'get_metrics',
    'get_metrics_content_type'
]
