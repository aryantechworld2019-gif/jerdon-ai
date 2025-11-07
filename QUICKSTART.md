# 🚀 Jerdon AI - Week 6 Quick Start Guide

## What You've Built

**Week 6: Monitoring, Analytics & Logging** - A production-ready backend with comprehensive observability.

### ✅ Features Implemented

- **📝 Structured Logging**: JSON logs for production, colored console for development
- **📊 Prometheus Metrics**: Track API performance, business metrics, and system resources
- **📈 Analytics Service**: User behavior tracking and platform insights
- **🏥 Health Checks**: Service health monitoring
- **🔍 Request Tracing**: Unique request IDs through entire request lifecycle

## 🎯 Quick Start (5 minutes)

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Dependencies installed:**
- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `motor` - Async MongoDB driver (optional)
- `prometheus-client` - Metrics collection
- `structlog` - Structured logging
- `colorlog` - Colored console logs
- `psutil` - System metrics

### 2. Run the Server

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
✅ Configuration loaded for development environment
✅ Logging configured for development environment
⚠️  MongoDB not available: ...
Running in demo mode without database
✅ CORS configured for: ['http://localhost:3000']
✅ Jerdon AI Backend initialized successfully
📊 Metrics endpoint: /metrics
🏥 Health endpoint: /health
📈 Analytics endpoint: /analytics/platform
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3. Test the API

Open a new terminal and test the endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Prometheus metrics
curl http://localhost:8000/metrics

# Demo chat (tracks metrics)
curl -X POST http://localhost:8000/demo/chat

# Demo upload (tracks metrics)
curl -X POST http://localhost:8000/demo/upload

# Demo registration (tracks metrics + analytics)
curl -X POST http://localhost:8000/demo/register
```

## 📊 Exploring the Features

### 1. Health Monitoring

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-07T23:05:00Z",
  "version": "1.0.0",
  "environment": "development",
  "services": {
    "mongodb": "not configured"
  }
}
```

### 2. Prometheus Metrics

```bash
curl http://localhost:8000/metrics | head -50
```

**Key metrics you'll see:**
```
# API Requests
api_requests_total{method="POST",endpoint="/demo/chat",status="200"} 5.0

# Request Duration
api_request_duration_seconds_bucket{endpoint="/demo/chat",le="0.1"} 5.0

# Business Metrics
chat_requests_total{user_plan="Trial",has_context="false"} 5.0
file_uploads_total{user_plan="Trial",file_type="pdf"} 3.0
user_registrations_total{plan="Trial"} 2.0

# System Metrics
system_cpu_usage_percent 45.2
system_memory_usage_bytes 2147483648
```

### 3. View Logs

```bash
# Watch logs in real-time
tail -f backend/logs/development.log

# Search for errors
grep "ERROR" backend/logs/development.log

# View request tracking
grep "Request completed" backend/logs/development.log
```

**Log entries include:**
- Request ID (unique per request)
- Duration in milliseconds
- User context (when authenticated)
- Endpoint and method
- Status code

### 4. Request Tracing

Every request gets a unique ID. Watch the flow:

```bash
# Make a request
curl -X POST http://localhost:8000/demo/chat

# In logs you'll see:
# Request started - request_id: 123e4567-e89b-12d3-a456-426614174000
# Processing... - request_id: 123e4567-e89b-12d3-a456-426614174000
# Request completed - request_id: 123e4567-e89b-12d3-a456-426614174000
```

## 🧪 Testing Demo Endpoints

### Generate Some Traffic

Run this script to generate metrics:

```bash
# Demo chat (5 times)
for i in {1..5}; do curl -X POST http://localhost:8000/demo/chat; done

# Demo upload (3 times)
for i in {1..3}; do curl -X POST http://localhost:8000/demo/upload; done

# Demo registration (2 times)
for i in {1..2}; do curl -X POST http://localhost:8000/demo/register; done

# View updated metrics
curl http://localhost:8000/metrics | grep -E "(chat_requests|file_uploads|user_registrations)"
```

## 📈 Metrics Visualization

### Option 1: Prometheus + Grafana (Full Stack)

1. **Install Prometheus:**
```bash
# Download Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvfz prometheus-2.45.0.linux-amd64.tar.gz
cd prometheus-2.45.0.linux-amd64
```

2. **Configure Prometheus** (`prometheus.yml`):
```yaml
scrape_configs:
  - job_name: 'jerdon-ai'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

3. **Run Prometheus:**
```bash
./prometheus --config.file=prometheus.yml
# Access at http://localhost:9090
```

4. **Query metrics in Prometheus:**
- `rate(api_requests_total[5m])` - Request rate
- `histogram_quantile(0.95, api_request_duration_seconds_bucket)` - P95 latency
- `chat_requests_total` - Total chat requests

### Option 2: Simple Metrics View

```bash
# Watch metrics update in real-time
watch -n 1 'curl -s http://localhost:8000/metrics | grep -A 1 "chat_requests\|file_uploads\|user_registrations"'
```

## 🔧 Configuration

### Environment Variables

Create `backend/.env`:

```bash
# Environment (development or production)
ENVIRONMENT=development

# MongoDB (optional - app works without it)
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=jerdon_ai_dev

# CORS
ALLOWED_ORIGINS=http://localhost:3000

# Admin API Key (for analytics endpoints)
ADMIN_API_KEY=your_secure_admin_key_here

# Redis (optional)
REDIS_ENABLED=false
```

### Production Mode

To run in production mode with JSON logging:

```bash
# Set environment to production
ENVIRONMENT=production uvicorn main:app --host 0.0.0.0 --port 8000

# Logs will be in JSON format:
# {"timestamp": "2025-11-07T23:05:00Z", "level": "INFO", "logger": "main", ...}
```

## 📁 Project Structure

```
jerdon-ai/
├── backend/
│   ├── main.py                     # FastAPI application
│   ├── config.py                   # Configuration
│   ├── logging_config.py           # Logging setup
│   ├── requirements.txt            # Dependencies
│   ├── test_api.py                 # Test script
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── request_context.py      # Request tracking
│   ├── monitoring/
│   │   ├── __init__.py
│   │   └── metrics.py              # Prometheus metrics
│   ├── analytics/
│   │   ├── __init__.py
│   │   └── analytics_service.py    # Analytics
│   └── logs/
│       └── development.log         # Log files
├── README.md                       # Full documentation
└── QUICKSTART.md                   # This file
```

## 🎓 What Each Component Does

### 1. `main.py` - FastAPI Application
- Defines all API endpoints
- Sets up middleware (CORS, request tracking)
- Handles startup/shutdown
- Integrates metrics and logging

### 2. `logging_config.py` - Logging System
- Configures structured logging
- JSON format for production
- Colored console for development
- Log rotation and file handling

### 3. `middleware/request_context.py` - Request Tracking
- Generates unique request IDs
- Tracks request duration
- Logs request start/completion
- Handles errors

### 4. `monitoring/metrics.py` - Prometheus Metrics
- Defines all metrics (counters, gauges, histograms)
- Provides decorator for tracking
- Collects system metrics (CPU, memory)
- Exports metrics in Prometheus format

### 5. `analytics/analytics_service.py` - Analytics
- Tracks user events
- Platform-wide analytics
- User behavior insights
- Retention metrics

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
kill $(lsof -t -i:8000)

# Or use a different port
uvicorn main:app --reload --port 8001
```

### Dependencies Not Installing
```bash
# Use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Metrics Not Showing
```bash
# Verify prometheus-client is installed
pip list | grep prometheus

# Check metrics endpoint
curl http://localhost:8000/metrics | head -20
```

### Logs Not Appearing
```bash
# Check logs directory exists
ls -la backend/logs/

# Create if missing
mkdir -p backend/logs

# Check permissions
chmod 755 backend/logs
```

## 📚 Next Steps

### Week 7: Deployment & DevOps
- Docker containerization
- CI/CD pipeline setup
- Cloud deployment (AWS/GCP/Azure)
- Production database setup
- SSL/TLS configuration
- Domain configuration

### Week 8: Production Launch
- Load testing
- Security audit
- Backup strategy
- Monitoring alerts
- User documentation

## 🎯 Key Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Root endpoint |
| `/health` | GET | Health check |
| `/metrics` | GET | Prometheus metrics |
| `/analytics/platform` | GET | Platform analytics (admin) |
| `/demo/chat` | POST | Demo chat (with metrics) |
| `/demo/upload` | POST | Demo upload (with metrics) |
| `/demo/register` | POST | Demo registration (with metrics + analytics) |

## 💡 Tips

1. **Monitor metrics regularly** - Watch for performance degradation
2. **Check logs for errors** - Proactive issue detection
3. **Use request IDs** - Track requests end-to-end
4. **Set up alerts** - Get notified of issues
5. **Review analytics** - Understand user behavior

## 🎉 Success Criteria

You've successfully completed Week 6 if you can:

- ✅ Start the server without errors
- ✅ Access `/health` endpoint
- ✅ View Prometheus metrics at `/metrics`
- ✅ See metrics increment after calling demo endpoints
- ✅ Find request logs in `backend/logs/development.log`
- ✅ Track individual requests via request ID
- ✅ See colored log output in console

## 📞 Need Help?

Common commands:

```bash
# Start server
uvicorn main:app --reload

# Watch logs
tail -f backend/logs/development.log

# Test endpoint
curl http://localhost:8000/health

# View metrics
curl http://localhost:8000/metrics | less

# Generate test traffic
for i in {1..10}; do curl -X POST http://localhost:8000/demo/chat; done
```

---

**Congratulations!** 🎉 You now have a production-ready backend with comprehensive monitoring, logging, and analytics! Your application is observable, trackable, and ready for the next phase of deployment.
