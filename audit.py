from datetime import datetime
import os

# Base para salvar o log de auditoria no mesmo diretório deste arquivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIT_PATH = os.path.join(BASE_DIR, "audit_log.txt")

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
