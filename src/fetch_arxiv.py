import requests
import feedparser

def fetch_arxiv(url):
    response = requests.get(url, timeout=30)
    parsed = feedparser.parse(response.content)

    papers = []
    for entry in parsed.entries:
        try:
            paper = {
                "title" : entry.get('title', 'Untitled'),
                "abstract" : entry.get('summary', ''),
                "link" : entry.get('link', ''),
                "authors" : [a.get('name', 'Unknown') for a in entry.get('authors', [])],
                "source": "arxiv",
                }
            papers.append(paper)
        except Exception:
            continue
    
    return papers
