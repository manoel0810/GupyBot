from groupManenger import JsonGroupManager
from gupy.engine import process
from emailEngine import sendEmails, sendLogEmail
from audit import timeSinceLastAudit, updateAuditTime

NEW_HIRING = 'Nova Vaga Detectada'
AUDIT_INTERVAL_HOUR = 6

def main() -> None:
    manager = JsonGroupManager()

    for group in manager.get_all_groups():
        print(f'\nGROUP ID: {group.groupId}')
        new, registered = process(group.url)
        if new:
            for _, html_formatado in new:
                sendEmails(NEW_HIRING, html_formatado, group.emails)

    if timeSinceLastAudit() >= AUDIT_INTERVAL_HOUR:
                ultima_vaga = next(iter(registered)) if registered else 'Nenhuma'
                sendLogEmail(
                        len(registered),
                        ultima_vaga
                )
                updateAuditTime()


if __name__ == '__main__':
    main()