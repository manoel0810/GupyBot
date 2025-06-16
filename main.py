import argparse
import os
from groupManenger import JsonGroupManager
from gupy.engine import process
from emailEngine import sendEmails, sendLogEmail
from audit import timeSinceLastAudit, updateAuditTime
from database import read, GUPY_DATASET
from datetime import datetime
from gupy.template import build_multiple

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
        # ATUALIZADO: Lógica para múltiplas chaves
        print(f'\nGROUP ID: {group.groupId} | KEYS: {", ".join(group.keys)}')
        if group.skip:
            print('skip group...')
            continue

        # Lista para agregar vagas de todas as palavras-chave do grupo
        all_new_jobs_for_group = []
        # Conjunto para garantir que não adicionemos vagas duplicadas no mesmo e-mail
        seen_job_urls = set()

        for key in group.keys:
            novas_vagas, _ = process(key, group.remoteOnly)
            for vaga in novas_vagas:
                # Adiciona a vaga apenas se ainda não foi vista neste grupo
                if vaga['link'] not in seen_job_urls:
                    all_new_jobs_for_group.append(vaga)
                    seen_job_urls.add(vaga['link'])
        
        # Se encontrou alguma vaga nova para o grupo, envia o e-mail consolidado
        if all_new_jobs_for_group:
            print(f'--> Total de {len(all_new_jobs_for_group)} vagas novas encontradas para o grupo {group.groupId}.')
            html_unico = build_multiple(all_new_jobs_for_group)
            sendEmails(NEW_HIRING, html_unico, group.emails)
        else:
            print(f'--> Nenhuma vaga nova encontrada para o grupo {group.groupId}.')


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