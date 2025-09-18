# setup_groups.py
import os
import database
import main

database.init_db()  # Inicializa o banco de dados e cria as tabelas se não existirem
main.migrate_from_json()  # Migra os dados do JSON para o banco de dados

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "gupy_bot.db")

print("Grupos adicionados/atualizados com sucesso!")