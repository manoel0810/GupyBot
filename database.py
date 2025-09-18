# database.py
import sqlite3
import os
from datetime import datetime
from typing import List, Set, Any, Dict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "gupy_bot.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Tabela para armazenar as URLs já visitadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visited_urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Tabela para os grupos de busca
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER UNIQUE NOT NULL,
                keys TEXT NOT NULL,
                emails TEXT NOT NULL,
                remote_only BOOLEAN NOT NULL,
                skip BOOLEAN NOT NULL
            )
        ''')
        # Tabela para logs de auditoria
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                details TEXT
            )
        ''')
        conn.commit()

# --- Funções para URLs Visitadas ---

def get_visited_urls() -> Set[str]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM visited_urls")
        return {row[0] for row in cursor.fetchall()}

def add_visited_url(url: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO visited_urls (url) VALUES (?)", (url,))
        conn.commit()

# --- Funções para Grupos ---

def add_or_update_group(group_data: Dict[str, Any]) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO groups (group_id, keys, emails, remote_only, skip)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            group_data['groupId'],
            ','.join(group_data['keys']),
            ','.join(group_data['emails']),
            group_data['remoteOnly'],
            group_data['skip']
        ))
        conn.commit()

def get_all_groups() -> List[Dict[str, Any]]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT group_id, keys, emails, remote_only, skip FROM groups")
        groups = []
        for row in cursor.fetchall():
            groups.append({
                "groupId": row[0],
                "keys": row[1].split(','),
                "emails": row[2].split(','),
                "remoteOnly": bool(row[3]),
                "skip": bool(row[4])
            })
        return groups

# --- Funções de Auditoria ---

def log_audit_event(event_type: str, details: str = "") -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO audit_logs (event_type, details) VALUES (?, ?)",
            (event_type, details)
        )
        conn.commit()

def get_last_audit_time(event_type: str) -> datetime | None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp FROM audit_logs WHERE event_type = ? ORDER BY timestamp DESC LIMIT 1",
            (event_type,)
        )
        result = cursor.fetchone()
        if result:
            return datetime.fromisoformat(result[0])
        return None

def get_total_visited_urls() -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(id) FROM visited_urls")
        return cursor.fetchone()[0]

def get_last_visited_url() -> str:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM visited_urls ORDER BY timestamp DESC LIMIT 1")
        result = cursor.fetchone()
        return result[0] if result else "Nenhuma"