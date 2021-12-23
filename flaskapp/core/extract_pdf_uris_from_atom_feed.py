from typing import List
import feedparser
from bs4 import BeautifulSoup
import urllib

def extract_pdf_uris_from_atom_feed(feed:bytes) -> List:
    """Extract PDF URIs from an Atom feed

    Parameters:
    feed (str) : the feed from which extract PDF URIs, presented as a string

    Returns:
    List : List of PDF URIs as strings
    """
    soup = BeautifulSoup(feed, features="html.parser")
    pdf_uris = []
    for link in soup.find_all('link'):
        if link.get('title') == "pdf":
            pdf_uris.append(link.get('href'))
    return pdf_uris