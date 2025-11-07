"""
Jerdon AI Backend API
Week 6: Monitoring, Analytics & Logging Implementation
"""
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import logging

# Configuration
from config import (
    MONGODB_URI,
    MONGODB_DB_NAME,
    CORS_ORIGINS,
    ENVIRONMENT,
    APP_VERSION,
    ADMIN_API_KEY
)

# Logging
from logging_config import setup_logging, get_logger

# Middleware
from middleware.request_context import RequestContextMiddleware

# Monitoring
from monitoring.metrics import (
    get_metrics,
    get_metrics_content_type,
    track_api_request,
    chat_requests_total,
    file_uploads_total,
    user_registrations_total
)

# Analytics
from analytics.analytics_service import AnalyticsService

# Initialize logging
logger = get_logger(__name__)

# Database client (will be initialized in lifespan)
db_client = None
db = None
analytics_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    global db_client, db, analytics_service

    logger.info("🚀 Starting Jerdon AI Backend...")

    # Connect to MongoDB (optional for this demo)
    try:
        import motor.motor_asyncio
        db_client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
        db = db_client[MONGODB_DB_NAME]
        await db.command("ping")
        logger.info(f"✅ MongoDB connected: {MONGODB_DB_NAME}")

        # Initialize analytics service
        analytics_service = AnalyticsService(db)
        logger.info("✅ Analytics service initialized")
    except Exception as e:
        logger.warning(f"⚠️  MongoDB not available: {e}")
        logger.info("Running in demo mode without database")

    yield

    # Shutdown
    if db_client:
        db_client.close()
        logger.info("✅ MongoDB connection closed")

    logger.info("👋 Jerdon AI Backend shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="Jerdon AI Backend API",
    description="RAG-based AI assistant with comprehensive monitoring",
    version=APP_VERSION,
    lifespan=lifespan
)

# Add request context middleware
app.add_middleware(RequestContextMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"✅ CORS configured for: {CORS_ORIGINS}")

# ==================== Health & Monitoring Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Jerdon AI Backend API",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    Returns application health status.
    """
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "services": {}
    }

    # Check MongoDB
    if db:
        try:
            await db.command("ping")
            health_data["services"]["mongodb"] = "healthy"
        except Exception as e:
            health_data["services"]["mongodb"] = f"unhealthy: {str(e)}"
            health_data["status"] = "degraded"
    else:
        health_data["services"]["mongodb"] = "not configured"

    return health_data

@app.get("/metrics")
async def metrics():
    """
    Prometheus metrics endpoint.
    Returns metrics in Prometheus exposition format.
    """
    return Response(
        content=get_metrics(),
        media_type=get_metrics_content_type()
    )

# ==================== Analytics Endpoints (Admin Only) ====================

@app.get("/analytics/platform")
async def get_platform_analytics(
    days: int = 30,
    api_key: str = Header(...)
):
    """
    Get platform-wide analytics (admin only).

    Args:
        days: Number of days to analyze (default: 30)

    Headers:
        api_key: Admin API key
    """
    if api_key != ADMIN_API_KEY:
        raise HTTPException(401, "Invalid API key")

    if not analytics_service:
        raise HTTPException(503, "Analytics service not available")

    try:
        analytics = await analytics_service.get_platform_analytics(days)
        return analytics
    except Exception as e:
        logger.error(f"Error getting platform analytics: {e}", exc_info=True)
        raise HTTPException(500, "Error retrieving analytics")

# ==================== Demo Endpoints ====================

@app.post("/demo/chat")
@track_api_request("/demo/chat")
async def demo_chat():
    """Demo chat endpoint with metrics tracking"""

    # Track business metric
    chat_requests_total.labels(
        user_plan="Trial",
        has_context="false"
    ).inc()

    return {
        "message": "This is a demo response",
        "metrics": "Request tracked in Prometheus metrics"
    }

@app.post("/demo/upload")
@track_api_request("/demo/upload")
async def demo_upload():
    """Demo upload endpoint with metrics tracking"""

    # Track business metric
    file_uploads_total.labels(
        user_plan="Trial",
        file_type="pdf"
    ).inc()

    return {
        "message": "Demo upload successful",
        "metrics": "Upload tracked in Prometheus metrics"
    }

@app.post("/demo/register")
@track_api_request("/demo/register")
async def demo_register():
    """Demo registration endpoint with metrics tracking"""

    # Track business metric
    user_registrations_total.labels(plan="Trial").inc()

    # Track analytics event
    if analytics_service:
        await analytics_service.track_event(
            "demo_user",
            "user_registered",
            {"plan": "Trial"}
        )

    return {
        "message": "Demo registration successful",
        "metrics": "Registration tracked in Prometheus and analytics"
    }

logger.info("✅ Jerdon AI Backend initialized successfully")
logger.info(f"📊 Metrics endpoint: /metrics")
logger.info(f"🏥 Health endpoint: /health")
logger.info(f"📈 Analytics endpoint: /analytics/platform")
