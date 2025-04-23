from datetime import datetime, timedelta
import os

AUDIT_PATH = os.path.join(os.getcwd(), "audit_log.txt")

def timeSinceLastAudit():
    if not os.path.exists(AUDIT_PATH):
        return float('inf')  # Se não existe, força envio
    with open(AUDIT_PATH, 'r') as f:
        last_execution_str = f.read().strip()
    last_execution = datetime.fromisoformat(last_execution_str)
    return (datetime.now() - last_execution).total_seconds() / 3600  # horas

def updateAuditTime():
    with open(AUDIT_PATH, 'w') as f:
        f.write(datetime.now().isoformat())