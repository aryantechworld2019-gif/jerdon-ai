"""
Analytics service for tracking user behavior and system performance.
"""
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Service for analytics and insights"""

    def __init__(self, db):
        self.db = db

    async def track_event(
        self,
        user_id: str,
        event_type: str,
        properties: Dict[str, Any] = None
    ):
        """Track an analytics event"""
        try:
            analytics_collection = self.db.get_collection("analytics_events")

            event = {
                "user_id": user_id,
                "event_type": event_type,
                "properties": properties or {},
                "timestamp": datetime.now(timezone.utc)
            }

            await analytics_collection.insert_one(event)

        except Exception as e:
            logger.error(f"Error tracking event: {e}", exc_info=True)

    async def get_platform_analytics(
        self,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get platform-wide analytics"""
        try:
            start_date = datetime.now(timezone.utc) - timedelta(days=days)

            users_collection = self.db.get_collection("users")

            total_users = await users_collection.count_documents({})
            active_users = await users_collection.count_documents({
                "lastLoginAt": {"$gte": start_date}
            })

            # Users by plan
            plan_pipeline = [
                {
                    "$group": {
                        "_id": "$plan",
                        "count": {"$sum": 1}
                    }
                },
                {"$sort": {"count": -1}}
            ]

            users_by_plan = await users_collection.aggregate(
                plan_pipeline
            ).to_list(None)

            return {
                "period_days": days,
                "users": {
                    "total": total_users,
                    "active": active_users,
                    "active_percentage": round((active_users / total_users * 100), 1) if total_users > 0 else 0,
                    "by_plan": users_by_plan
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        except Exception as e:
            logger.error(f"Error getting platform analytics: {e}", exc_info=True)
            return {}

__all__ = ['AnalyticsService']
