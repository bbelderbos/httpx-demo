from pathlib import Path
import requests
from bs4 import BeautifulSoup

API_URL = "https://codechalleng.es/api/articles/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
}
PYBITES = ("https://pybit.es", "http://pybit.es")


def get_article_links():
    resp = requests.get(API_URL)
    resp.raise_for_status()
    uniq_links = set()
    for link in [art["link"] for art in resp.json()[:10]]:
        links = _get_links(link)
        uniq_links.update(links)
    Path("links.txt").write_text("\n".join(uniq_links))


def _get_links(url):
    resp = requests.get(url, headers=HEADERS)
    if not resp.ok:
        print("cannot retrieve", url)
        return set()
    else:
        soup = BeautifulSoup(resp.content, "html.parser")
        links = {
            link["href"] for link in soup.find_all("a", href=True)
            if link["href"].startswith(PYBITES)
        }
        return links


get_article_links()
