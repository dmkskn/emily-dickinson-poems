"""Scrapes all Emily Dickinson poems."""
import json
from typing import Dict, List, NamedTuple, Optional
from dataclasses import dataclass, field, asdict
from requests_html import HTMLSession


session = HTMLSession()


@dataclass
class Poem:
    """
    Represents a single poem.
        - `title` — a poem title.
        - `content` - a poem text.
    """

    title: str
    content: Optional[str] = field(default=None)


class _PoemWikipediaPage(NamedTuple):
    """
    Keeps the data about a poem webpage.
        - `title` — a poem title.
        - `url` — an url address to Wikipedia page with this poem.
    """

    title: str
    url: str


def _parse_poem_text(url: str) -> Optional[str]:
    """Parses the text of a poem from a page."""

    print(f"Parsing: {url}")

    response = session.get(url)
    poem_html = response.html.find(".poem", first=True)

    if poem_html:
        return poem_html.text
    else:
        print(f"No poem in {url}")
        return None


def _parse_poems_table() -> List[_PoemWikipediaPage]:
    """Parses a table with all poems."""

    print(f"Parsing table...")

    response = session.get("https://en.wikipedia.org/wiki/List_of_Emily_Dickinson_poems")
    html_links = response.html.find("table.wikitable > tbody > tr > td:first-child > a")

    return [_PoemWikipediaPage(link.text, link.attrs["href"]) for link in html_links]


# Public Staff Here


def save_result_as_json(data: List[Dict]) -> None:
    """Save `data` to json file."""
    with open("emily-dickinson.json", "w", encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False)


def prepare_for_saving(poems: List[Poem]) -> List[Dict]:
    """Transforms poems to dicts in the list."""
    return [asdict(poem) for poem in poems]


def get_poems() -> List[Poem]:
    """Generates all poems."""
    poem_wiki_pages = _parse_poems_table()
    return [Poem(page.title, _parse_poem_text(page.url)) for page in poem_wiki_pages]


# Run Script

poems = get_poems()
data = prepare_for_saving(poems)
save_result_as_json(data)
