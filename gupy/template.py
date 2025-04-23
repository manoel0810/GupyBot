from bs4 import BeautifulSoup

def build(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    link = soup.find('a')['href'] if soup.find('a') else '#'
    empresa = soup.find('p', class_='sc-bBXxYQ')
    titulo = soup.find('h3')
    data_publicacao = soup.find('p', class_='sc-bBXxYQ eJcDNr sc-d9e69618-0 iUzUdL')
    logo_img = soup.find('img')

    detalhes = soup.find_all('span', class_='sc-23336bc7-1')

    local = detalhes[0].text if len(detalhes) > 0 else 'Não informado'
    modelo_trabalho = detalhes[1].text if len(detalhes) > 1 else 'Não informado'
    tipo_vaga = detalhes[2].text if len(detalhes) > 2 else 'Não informado'
    inclusiva_pcd = detalhes[3].text if len(detalhes) > 3 else None

    empresa = empresa.text.strip() if empresa else 'Empresa não informada'
    titulo = titulo.text.strip() if titulo else 'Título não informado'
    data_publicacao = data_publicacao.text.strip() if data_publicacao else 'Data não informada'
    logo_url = 'https://portal.gupy.io' + logo_img['src'] if logo_img else ''

    pcd_html = f'<p><strong>Inclusiva para PcD</strong></p>' if inclusiva_pcd else ''

    html = f'''
    <div style="border:1px solid #ccc;padding:16px;border-radius:8px;font-family:sans-serif;max-width:600px;">
        <div style="display:flex;align-items:center;">
            <img src="{logo_url}" alt="Logo da empresa" width="48" height="48" style="margin-right:12px;border-radius:8px;">
            <div>
                <h2 style="margin:0;">{titulo}</h2>
                <p style="margin:4px 0;color:gray;">{empresa}</p>
            </div>
        </div>
        <p><strong>Local:</strong> {local}</p>
        <p><strong>Modelo:</strong> {modelo_trabalho}</p>
        <p><strong>Tipo:</strong> {tipo_vaga}</p>
        {pcd_html}
        <p style="color:gray;">📅 {data_publicacao}</p>
        <p><a href="{link}" style="color:#007bff;">🔗 Ver vaga completa</a></p>
    </div>
    '''
    return html
