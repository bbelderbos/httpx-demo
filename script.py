from pathlib import Path
from bs4 import BeautifulSoup
from typing import Union

import requests

API_URL = "https://codechalleng.es/api/articles/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
}
PYBITES = ("https://pybit.es", "http://pybit.es")


def get_article_links(*, max_num: Union[int, None] = None) -> list[str]:
    resp = requests.get(API_URL)
    links = [art["link"] for art in resp.json()]
    return links[:max_num] if max_num is not None else links


def store_links(links: dict[str, list[str]]) -> None:
    content = []
    for art, urls in sorted(links.items()):
        for u in sorted(urls):
            content.append(f"{art},{u}")
    Path("links.txt").write_text("\n".join(content))


def get_articles_html(articles: list[str]) -> dict[str, str]:
    contents = {}
    for art in articles:
        resp = requests.get(art, headers=HEADERS)
        contents[art] = resp.text
    return contents


def get_links_from_html(content: str) -> set[str]:
    soup = BeautifulSoup(content, "html.parser")
    links = {
        link["href"]
        for link in soup.find_all("a", href=True)
        if link["href"].startswith(PYBITES)
    }
    return links


def main() -> None:
    articles = get_article_links(max_num=50)
    links: dict[str, list[str]] = {art: [] for art in articles}
    contents = get_articles_html(articles)
    seen = set()
    for art, content in contents.items():
        art_links = get_links_from_html(content)

        new_art_links = []
        for al in art_links:
            if al in seen:
                continue
            seen.add(al)
            new_art_links.append(al)

        links[art].extend(new_art_links)

    store_links(links)


if __name__ == "__main__":
    main()
