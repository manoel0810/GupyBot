#template.py

def build(titulo: str, empresa: str, descricao: str, logo: str, link: str, local: str = "Não informado",
          modelo_trabalho: str = "Remoto", tipo_vaga: str = "Não informado", inclusiva_pcd: bool = False,
          data_publicacao: str = "") -> str:

    logo_url = logo if logo else ""
    pcd_html = '<p><strong>Inclusiva para PcD</strong></p>' if inclusiva_pcd else ''

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
