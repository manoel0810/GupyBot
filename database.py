import os

# Define o diretório de trabalho como o diretório atual + "datasets"
WORK_DIR = os.path.join(os.getcwd(), "datasets")
os.makedirs(WORK_DIR, exist_ok=True)

#DATASETS NAME
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