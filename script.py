import asyncio
from pathlib import Path
import httpx
from bs4 import BeautifulSoup

API_URL = "https://codechalleng.es/api/articles/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
}
PYBITES = ("https://pybit.es", "http://pybit.es")


async def get_article_links(*, max_num=None):
    resp = httpx.get(API_URL)
    links = [art["link"] for art in resp.json()]
    return links[:max_num] if max_num is not None else links


def store_links(links):
    Path("links.txt").write_text("\n".join(links))


async def get_articles_html(articles):
    async with httpx.AsyncClient(headers=HEADERS) as client:
        contents = []
        for art in articles:
            resp = await client.get(art)
            contents.append(resp.content)
        return contents


async def get_links_from_html(content):
    soup = BeautifulSoup(content, "html.parser")
    links = {
        link["href"]
        for link in soup.find_all("a", href=True)
        if link["href"].startswith(PYBITES)
    }
    return links


async def main():
    articles = await get_article_links(max_num=10)
    links = set(articles)
    contents = await get_articles_html(articles)
    for content in contents:
        art_links = await get_links_from_html(content)
        links.update(art_links)
    store_links(links)


if __name__ == "__main__":
    asyncio.run(main())
