import argparse
import os
from groupManenger import JsonGroupManager
from gupy.engine import process
from emailEngine import sendEmails, sendLogEmail
from audit import timeSinceLastAudit, updateAuditTime
from database import read, GUPY_DATASET
from datetime import datetime

NEW_HIRING = 'Nova Vaga Detectada'
AUDIT_INTERVAL_HOUR = 6

def logHeaders() -> None:
    print('')
    print('*'*30, 'Work Info', '*'*30)
    print(f'Work Dir: {os.getcwd()}')

    agora = datetime.now()
    data_formatada = agora.strftime('%Y-%m-%d %H:%M:%S')

    print(f'Date: {data_formatada}')
    print('*'*71, '\n')

def main(base_path: str) -> None:
    os.chdir(base_path)

    logHeaders()
    manager = JsonGroupManager()

    for group in manager.get_all_groups():
        print(f'\nGROUP ID: {group.groupId} | KEY: {group.key}')
        if group.skip:
            print('skip group...')
            continue

        new, _ = process(group.key, group.remoteOnly)
        if new:
            for _, html_formatado in new:
                sendEmails(NEW_HIRING, html_formatado, group.emails)

    if timeSinceLastAudit() >= AUDIT_INTERVAL_HOUR:
                regs = read(GUPY_DATASET)
                ultima_vaga = next(iter(regs)) if regs else 'Nenhuma'
                sendLogEmail(
                        len(regs),
                        ultima_vaga
                )
                updateAuditTime()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--basepath", 
        help="Caminho base do projeto",
        default=os.getcwd()
    )
    args = parser.parse_args()
    main(args.basepath)