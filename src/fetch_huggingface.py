import requests
from datetime import datetime

def fetch_huggingface(limit = 10):
    today = datetime.now().strftime("%Y-%m-%d")

    url = f"https://huggingface.co/api/daily_papers?date={today}&limit={limit}"

    response = requests.get(url)
    data = response.json()

    papers = []
    for item in data:
        paper = item.get("paper", {})
        papers.append(
            {
                "title": paper.get('title', ""),
                "abstract": paper.get('summary', ""),
                "link": f"https://arxiv.org/abs/{paper.get('id', '')}",
                "authors": [a['name'] for a in paper.get("authors", "")],
                "upvotes": paper.get('upvotes', 0),
                "source": "huggingface,"
            }
        )
    
    return papers