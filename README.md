# Jerdon AI - Week 6: Monitoring, Analytics & Logging

Production-ready RAG-based AI platform with comprehensive monitoring, analytics, and structured logging.

## 🎯 Week 6 Features Implemented

### ✅ Structured Logging
- **JSON logging** for production environments
- **Colored console logging** for development
- **Request context tracking** with unique request IDs
- **User context** in all logs
- **Log rotation** for efficient storage
- **Structured fields** for easy searching

### ✅ Application Monitoring
- **Prometheus metrics** for all API endpoints
- **Business metrics** tracking (chats, uploads, registrations)
- **System metrics** (CPU, memory usage)
- **Error tracking** with detailed context
- **Request duration** histograms
- **Active requests** gauges

### ✅ Analytics & Insights
- **Event tracking** for user actions
- **Platform analytics** (users, activity, retention)
- **User behavior** analysis
- **Admin dashboard** ready endpoints
- **Retention metrics** (7-day, 30-day)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Create Environment File

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Run the Backend

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## 📊 Monitoring Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00Z",
  "version": "1.0.0",
  "environment": "development",
  "services": {
    "mongodb": "not configured"
  }
}
```

### Prometheus Metrics
```bash
curl http://localhost:8000/metrics
```

Returns metrics in Prometheus format including:
- `api_requests_total` - Total API requests by method, endpoint, and status
- `api_request_duration_seconds` - Request duration histogram
- `chat_requests_total` - Total chat requests by plan
- `file_uploads_total` - Total file uploads by plan and type
- `user_registrations_total` - Total user registrations
- `system_cpu_usage_percent` - CPU usage
- `system_memory_usage_bytes` - Memory usage
- `errors_total` - Total errors by type

### Platform Analytics (Admin Only)
```bash
curl -H "api-key: your_admin_key" \
  http://localhost:8000/analytics/platform?days=30
```

Returns:
```json
{
  "period_days": 30,
  "users": {
    "total": 150,
    "active": 95,
    "active_percentage": 63.3,
    "by_plan": [...]
  },
  "timestamp": "2025-01-15T10:30:00Z"
}
```

## 🧪 Demo Endpoints

Test the monitoring system with demo endpoints:

### Demo Chat
```bash
curl -X POST http://localhost:8000/demo/chat
```

### Demo Upload
```bash
curl -X POST http://localhost:8000/demo/upload
```

### Demo Registration
```bash
curl -X POST http://localhost:8000/demo/register
```

Each demo endpoint tracks metrics that you can see in `/metrics`.

## 📝 Logging

### Development Logs
Logs are written to `backend/logs/development.log` with colored output to console.

### View Logs
```bash
# Watch logs in real-time
tail -f backend/logs/development.log

# Search logs
grep "Request completed" backend/logs/development.log

# Filter by level
grep "ERROR" backend/logs/development.log
```

### Log Format (Development)
```
2025-01-15 10:30:00 [INFO] main:125 - Request completed
2025-01-15 10:30:01 [ERROR] main:156 - Request failed
```

### Log Format (Production - JSON)
```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "INFO",
  "logger": "main",
  "message": "Request completed",
  "request_id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user123",
  "environment": "production"
}
```

## 📈 Metrics Integration

### Prometheus Setup
Add this to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'jerdon-ai'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

### Grafana Dashboard
Import metrics to Grafana for visualization:
- Request rates and latencies
- Error rates
- System resource usage
- Business metrics (signups, uploads, etc.)

## 🔧 Configuration

### Environment Variables

```bash
# Required
ENVIRONMENT=development          # development or production

# Optional
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=jerdon_ai_dev
ALLOWED_ORIGINS=http://localhost:3000
ADMIN_API_KEY=your_secure_key
REDIS_ENABLED=false
```

## 📦 Project Structure

```
jerdon-ai/
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration management
│   ├── logging_config.py          # Structured logging setup
│   ├── requirements.txt           # Python dependencies
│   ├── middleware/
│   │   └── request_context.py     # Request tracking middleware
│   ├── monitoring/
│   │   └── metrics.py             # Prometheus metrics
│   ├── analytics/
│   │   └── analytics_service.py   # Analytics & insights
│   └── logs/                      # Log files (auto-created)
└── README.md
```

## 🎓 What You've Built

### Week 6 Accomplishments

✅ **Structured Logging System**
- JSON logs for production
- Colored logs for development
- Request ID tracking
- User context in logs

✅ **Comprehensive Monitoring**
- Prometheus metrics integration
- API performance tracking
- Business metrics
- System resource monitoring

✅ **Analytics Platform**
- Event tracking system
- Platform-wide analytics
- User behavior insights
- Retention metrics

✅ **Production-Ready Infrastructure**
- Health check endpoints
- Graceful startup/shutdown
- Error tracking
- Performance monitoring

## 🔍 Monitoring Best Practices

### 1. Request Tracking
Every request gets a unique ID that flows through all logs:
```
[INFO] Request started - request_id: 123e4567...
[INFO] Processing chat - request_id: 123e4567..., user_id: user123
[INFO] Request completed - request_id: 123e4567..., duration_ms: 250
```

### 2. Business Metrics
Track key business events:
- User registrations (`user_registrations_total`)
- Chat requests (`chat_requests_total`)
- File uploads (`file_uploads_total`)
- Plan upgrades (`plan_upgrades_total`)

### 3. Performance Monitoring
Monitor request performance:
- Request duration percentiles (p50, p95, p99)
- Error rates by endpoint
- Active concurrent requests

### 4. System Health
Track system resources:
- CPU usage
- Memory usage
- Disk usage (when integrated)

## 🚦 Health Check Integration

### Kubernetes Liveness Probe
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

### Docker Healthcheck
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

## 📚 Next Steps

### Week 7: Deployment & DevOps
- Docker containerization
- CI/CD pipeline
- Cloud deployment (AWS/GCP/Azure)
- Database setup
- SSL/TLS configuration

### Week 8: Production Launch
- Load testing
- Security hardening
- Backup strategy
- Monitoring alerts
- Documentation

## 🐛 Troubleshooting

### Metrics Not Showing Up
```bash
# Check if Prometheus dependencies are installed
pip install prometheus-client psutil

# Verify metrics endpoint
curl http://localhost:8000/metrics | head -20
```

### Logs Not Appearing
```bash
# Check logs directory exists
ls -la backend/logs/

# Check log file
cat backend/logs/development.log
```

### MongoDB Connection Issues
The app works without MongoDB in demo mode. For full functionality:
```bash
# Install MongoDB locally or use MongoDB Atlas
# Update MONGODB_URI in .env
```

## 📞 Support

For issues or questions:
- Check logs: `backend/logs/development.log`
- View metrics: `http://localhost:8000/metrics`
- Health status: `http://localhost:8000/health`

## 🎉 Congratulations!

You've successfully implemented Week 6 of the Jerdon AI platform with:
- ✅ Production-grade logging
- ✅ Comprehensive monitoring
- ✅ Analytics infrastructure
- ✅ Health checks
- ✅ Metrics tracking

Your application is now observable, monitorable, and ready for production deployment! 🚀
