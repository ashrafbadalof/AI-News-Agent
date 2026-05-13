import requests
from datetime import datetime

def fetch_huggingface(limit = 10):
    today = datetime.now().strftime("%Y-%m-%d")

    url = f"https://huggingface.co/api/daily_papers?date={today}&limit={limit}"

    response = requests.get(url, timeout=30)
    data = response.json()

    papers = []
    for item in data:
        try:
            paper = item.get("paper", {})
            papers.append(
                {
                    "title": paper.get('title', "Untitled"),
                    "abstract": paper.get('summary', ""),
                    "ai_summary": paper.get('ai_summary', "No summary available"),
                    "link": f"https://arxiv.org/abs/{paper.get('id', '')}",
                    "authors": [a.get('name', 'Unknown') for a in paper.get("authors", [])],
                    "upvotes": paper.get('upvotes', 0),
                    "source": "huggingface",
                }
            )
        except Exception:
            continue
    
    return papers