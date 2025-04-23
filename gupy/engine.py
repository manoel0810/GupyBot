import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
from gupy.template import build
from database import read, saveLine, GUPY_DATASET

def search(url: str):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--remote-debugging-port=9222")

    if os.name == 'nt':
        navegador = webdriver.Chrome(options=options)
    else:
        service = Service(os.path.join(os.getcwd(), "chromedriver"))
        navegador = webdriver.Chrome(service=service, options=options)
        if not os.path.isfile(chromedriver_path):
            raise FileNotFoundError("chromedriver não encontrado no diretório atual!")

    navegador.get(url)
    time.sleep(10)

    page_source = navegador.page_source
    navegador.quit()

    print('SEARCH END')
    return page_source

def parser(page):
    print('PARSER INIT')
    soup = BeautifulSoup(page, 'html.parser')

    vagas_existentes = read(GUPY_DATASET)
    novas_vagas = []

    for div_vaga in soup.select('div[class^="sc-4d881605-0"]'):
        link = div_vaga.find('a')
        if not link or not link.has_attr('href'):
            continue

        url = link['href']
        if url not in vagas_existentes:
            html_vaga_formatado = build(str(link))
            novas_vagas.append((url, html_vaga_formatado))
            saveLine(GUPY_DATASET, url)

    print('PARSER END')
    return novas_vagas, vagas_existentes

def process(url: str) -> tuple:
    print(f'INITIALIZING SEARCH FOR ({url})\n')
    page = search(url)
    return parser(page)