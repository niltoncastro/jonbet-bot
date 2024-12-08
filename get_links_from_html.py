from bs4 import BeautifulSoup

from display_message import display_message
from process_tournament import process_tournament


def get_links_from_html(html_source):
    """Extrai os links da página HTML."""
    try:
        soup = BeautifulSoup(html_source, 'html.parser')
        links = []
        for link in soup.find_all('link', href=True):
            if "2359744937144225792" in link['href'].lower():
                links.append(link['href'])

                # processa liga Venezuela
                codigo_liga = "2361937986599399439"
                process_tournament(link['href'], codigo_liga)

                # processa liga dos Campeoes
                # codigo_liga = "2424576288317644818"
                # process_tournament(link['href'], codigo_liga)

        return links
    except Exception as e:
        display_message(f"Erro ao processar o HTML: {str(e)}")
        return []
