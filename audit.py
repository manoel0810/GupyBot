# audit.py
from datetime import datetime, timedelta
from database import log_audit_event, get_last_audit_time

def timeSinceLastAudit(event_type: str) -> float:
    last_execution = get_last_audit_time(event_type)
    if not last_execution:
        return float('inf')  # Se não existe, força envio
    return (datetime.now() - last_execution).total_seconds() / 3600  # horas

def updateAuditTime(event_type: str, details: str = ""):
    log_audit_event(event_type, details)