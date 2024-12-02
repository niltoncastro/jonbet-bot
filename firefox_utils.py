



def get_links_from_html(html_source):
    try:
        soup = BeautifulSoup(html_source, 'html.parser')
        links = []
        for link in soup.find_all('link', href=True):
            if "https://api-a-c7818b61-600.sptpub.com/api/v3/" in link['href']:
                links.append(link['href'])
        return links
    except Exception as e:
        display_message(f"Erro ao processar o HTML: {str(e)}")
        return []
