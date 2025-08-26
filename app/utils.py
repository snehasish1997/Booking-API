from datetime import datetime
from zoneinfo import ZoneInfo

def to_tz(dt_utc: datetime, tz: str) -> datetime:
    """Convert a naive/UTC datetime to requested timezone aware datetime."""
    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=ZoneInfo("UTC"))
    try:
        return dt_utc.astimezone(ZoneInfo(tz))
    except Exception:
        # fallback to IST if tz invalid
        return dt_utc.astimezone(ZoneInfo("Asia/Kolkata"))
