"""API management module for tracking users, locations, and statistics.

This module provides functionality to track API usage, including:
- Request counts per endpoint
- Unique users (by IP)
- Location data for users
- Basic statistics

Data is stored in a SQLite database using SQLAlchemy.
"""

import os
from datetime import datetime
from typing import Dict, Any
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///api_stats.db", echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String, index=True)
    ip = Column(String, index=True)
    city = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def track_request(endpoint: str, ip: str, location: Dict[str, Any] = None):
    """Track a request in the database."""
    db = SessionLocal()
    try:
        log = RequestLog(
            endpoint=endpoint,
            ip=ip,
            city=location.get("city") if location else None
        )
        db.add(log)
        db.commit()
    finally:
        db.close()

def get_stats() -> Dict[str, Any]:
    """Return current statistics from the database."""
    db = SessionLocal()
    try:
        # Total requests
        total_requests = db.query(RequestLog).count()

        # Unique users
        unique_users = db.query(RequestLog.ip).distinct().count()

        # Endpoint counts
        from sqlalchemy import func
        endpoint_counts = db.query(RequestLog.endpoint, func.count(RequestLog.id)).group_by(RequestLog.endpoint).all()
        endpoints = {ep: count for ep, count in endpoint_counts}

        # Top locations
        location_counts = db.query(RequestLog.city, func.count(RequestLog.id)).filter(RequestLog.city.isnot(None)).group_by(RequestLog.city).all()
        top_locations = sorted(location_counts, key=lambda x: x[1], reverse=True)[:10]

        # Recent requests
        recent = db.query(RequestLog).order_by(RequestLog.timestamp.desc()).limit(10).all()
        recent_requests = [
            {
                "endpoint": r.endpoint,
                "ip": r.ip,
                "city": r.city,
                "timestamp": r.timestamp.isoformat()
            } for r in recent
        ]

        return {
            "total_requests": total_requests,
            "unique_users": unique_users,
            "endpoints": endpoints,
            "top_locations": top_locations,
            "recent_requests": recent_requests,
        }
    finally:
        db.close()
