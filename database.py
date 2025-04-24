import os

# Define o diretório de trabalho como o diretório onde este arquivo está + "datasets"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.join(BASE_DIR, "datasets")

# Garante que a pasta exista
os.makedirs(WORK_DIR, exist_ok=True)

# Nome do arquivo de dataset
GUPY_DATASET = "gupy.txt"

def getPath(keyName: str) -> str:
    return os.path.join(WORK_DIR, keyName)

def read(keyName: str) -> set:
    path = getPath(keyName)
    if not os.path.exists(path):
        return set()
    with open(path, 'r', encoding='utf-8') as f:
        return set(linha.strip() for linha in f)

def saveLine(keyName: str, line: str) -> None:
    path = getPath(keyName)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line + '\n')
