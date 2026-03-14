"""API management module for tracking users, locations, and statistics.

This module provides functionality to track API usage, including:
- Request counts per endpoint
- Unique users (by IP)
- Location data for users
- Basic statistics

Data is stored in-memory for simplicity; in production, use a database.
"""

import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any

# In-memory storage for stats (use a database in production)
stats: Dict[str, Any] = {
    "total_requests": 0,
    "endpoints": defaultdict(int),
    "unique_ips": set(),
    "locations": defaultdict(int),  # city -> count
    "recent_requests": [],  # list of recent request logs
}

STATS_FILE = Path(__file__).parent.parent.parent / "api_stats.json"


def load_stats():
    """Load stats from file if it exists."""
    if STATS_FILE.exists():
        with open(STATS_FILE, "r") as f:
            data = json.load(f)
            stats.update(data)
            stats["unique_ips"] = set(stats.get("unique_ips", []))
            stats["endpoints"] = defaultdict(int, stats.get("endpoints", {}))
            stats["locations"] = defaultdict(int, stats.get("locations", {}))


def save_stats():
    """Save stats to file."""
    data = stats.copy()
    data["unique_ips"] = list(stats["unique_ips"])
    data["endpoints"] = dict(stats["endpoints"])
    data["locations"] = dict(stats["locations"])
    with open(STATS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def track_request(endpoint: str, ip: str, location: Dict[str, Any] = None):
    """Track a request for statistics."""
    stats["total_requests"] += 1
    stats["endpoints"][endpoint] += 1
    stats["unique_ips"].add(ip)

    if location:
        city = location.get("city", "Unknown")
        stats["locations"][city] += 1

    # Keep only last 100 recent requests
    stats["recent_requests"].append({
        "endpoint": endpoint,
        "ip": ip,
        "city": location.get("city") if location else None,
        "timestamp": None,  # Could add datetime if needed
    })
    if len(stats["recent_requests"]) > 100:
        stats["recent_requests"].pop(0)

    save_stats()


def get_stats() -> Dict[str, Any]:
    """Return current statistics."""
    return {
        "total_requests": stats["total_requests"],
        "unique_users": len(stats["unique_ips"]),
        "endpoints": dict(stats["endpoints"]),
        "top_locations": sorted(stats["locations"].items(), key=lambda x: x[1], reverse=True)[:10],
        "recent_requests": stats["recent_requests"][-10:],  # Last 10
    }


# Load stats on import
load_stats()
