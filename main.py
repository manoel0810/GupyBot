# main.py
import argparse
import os
import json
from groupManenger import GroupManager
from gupy.engine import process
from emailEngine import sendEmails, sendLogEmail
from audit import timeSinceLastAudit, updateAuditTime
from database import init_db, get_total_visited_urls, get_last_visited_url, add_or_update_group
from datetime import datetime
from gupy.template import build_multiple

NEW_HIRING = 'Nova Vaga Detectada'
AUDIT_INTERVAL_HOUR = 24
AUDIT_EVENT_TYPE = "EMAIL_AUDITORIA"
OLD_GROUPS_FILE = "groups.json"

def logHeaders() -> None:
    print('')
    print('*'*30, 'Work Info', '*'*30)
    print(f'Work Dir: {os.getcwd()}')
    agora = datetime.now()
    data_formatada = agora.strftime('%Y-%m-%d %H:%M:%S')
    print(f'Date: {data_formatada}')
    print('*'*71, '\n')

def migrate_from_json():
    if not os.path.exists(OLD_GROUPS_FILE):
        return

    print("--> Encontrado 'groups.json'. Iniciando migração para o banco de dados...")
    try:
        with open(OLD_GROUPS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            groups = data.get("groups", [])
            for group in groups:
                add_or_update_group(group)
            
        os.rename(OLD_GROUPS_FILE, f"{OLD_GROUPS_FILE}.migrated")
        print(f"--> {len(groups)} grupos migrados com sucesso. O arquivo foi renomeado para 'groups.json.migrated'.")
    except Exception as e:
        print(f"Ocorreu um erro durante a migração do JSON: {e}")

def main(base_path: str) -> None:
    os.chdir(base_path)
    init_db()  # Garante que o banco de dados e as tabelas existam
    
    # Executa a migração dos grupos se o arquivo antigo existir
    migrate_from_json()

    logHeaders()
    manager = GroupManager()

    for group in manager.get_all_groups():
        print(f'\nGROUP ID: {group.groupId} | KEYS: {", ".join(group.keys)}')
        if group.skip:
            print('skip group...')
            continue

        all_new_jobs_for_group = []
        seen_job_urls = set()

        for key in group.keys:
            novas_vagas, _ = process(key, group.remoteOnly)
            for vaga in novas_vagas:
                if vaga['link'] not in seen_job_urls:
                    all_new_jobs_for_group.append(vaga)
                    seen_job_urls.add(vaga['link'])
        
        if all_new_jobs_for_group:
            print(f'--> Total de {len(all_new_jobs_for_group)} vagas novas encontradas para o grupo {group.groupId}.')
            html_unico = build_multiple(all_new_jobs_for_group)
            sendEmails(NEW_HIRING, html_unico, group.emails)
        else:
            print(f'--> Nenhuma vaga nova encontrada para o grupo {group.groupId}.')

    if timeSinceLastAudit(AUDIT_EVENT_TYPE) >= AUDIT_INTERVAL_HOUR:
        total_vagas = get_total_visited_urls()
        ultima_vaga = get_last_visited_url()
        sendLogEmail(
            total_vagas,
            ultima_vaga
        )
        updateAuditTime(AUDIT_EVENT_TYPE, f"Total de vagas no banco: {total_vagas}")
        print("--> Log de auditoria enviado.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--basepath", 
        help="Caminho base do projeto",
        default=os.getcwd()
    )
    args = parser.parse_args()
    main(args.basepath)