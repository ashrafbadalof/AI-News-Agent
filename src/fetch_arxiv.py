import requests
import feedparser

def fetch_arxiv(url):
    response = requests.get(url)
    parsed = feedparser.parse(response.content)

    papers = []

    for entry in parsed.entries:
        paper = {
            "title" : entry['title'],
            "abstract" : entry['summary'],
            "link" : entry['link'],
            "authors" : [a['name'] for a in entry['authors']],
            }
        papers.append(paper)
    
    return papers
