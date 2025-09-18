# gupy/engine.py
import requests
from database import get_visited_urls, add_visited_url

API_URL = "https://employability-portal.gupy.io/api/v1/jobs"

def fetch_jobs(query: str, remote_only: bool, limit: int = 10000):
    params = {
        "jobName": query,
        #"offset": 0,
        #"limit": limit,
        "isRemoteWork": str(remote_only).lower()
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json()

def process(key: str, remote_only: bool) -> tuple:
    print(f"BUSCANDO VAGAS PARA: {key}")

    data = fetch_jobs(key, remote_only)
    vagas = data.get("data", [])
    vagas_existentes = get_visited_urls()
    novas_vagas = []

    for vaga in vagas:
        vaga_url = vaga.get("jobUrl")
        if not vaga_url or vaga_url in vagas_existentes:
            continue

        vaga_dict = {
            "titulo": vaga.get("name", "Título não informado"),
            "empresa": vaga.get("careerPageName", "Empresa não informada"),
            "descricao": vaga.get("description", ""),
            "logo": vaga.get("careerPageLogo", ""),
            "link": vaga_url,
            "local": vaga.get("city", "Não informado"),
            "modelo_trabalho": vaga.get("workplaceType", "Não informado"),
            "tipo_vaga": vaga.get("type", "Não informado"),
            "inclusiva_pcd": bool(vaga.get("disabilities", False)),
            "data_publicacao": vaga.get("publishedDate", "").split("T")[0]
        }

        novas_vagas.append(vaga_dict)
        add_visited_url(vaga_url)

    print(f"{len(novas_vagas)} novas vagas encontradas.")
    return novas_vagas, vagas_existentes