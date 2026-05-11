import time
from src.fetch_arxiv import fetch_arxiv
from src.summarize import summarize_paper
from src.relevance import rate_relevance
from src.email_sender import send_digest_email

from datetime import datetime
from pathlib import Path

Path('digests').mkdir(exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
filename = f"digests/digest_{today}.md"

url = 'http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=30'

papers = fetch_arxiv(url=url)
for paper in papers:
    paper['score'] = rate_relevance(paper)
    time.sleep(0.5)

papers.sort(key=lambda p: p['score'], reverse=True)
top_papers = papers[:5]

with open(filename, 'w', encoding='utf-8') as f:
    f.write(f'# AI Research Digest {today}\n\n')
    f.write(f'Reviewed {len(papers)} papers, showing top {len(top_papers)} by relevance. \n\n')

    for paper in top_papers:
        f.write(f'## {paper["title"]} \n')
        f.write(f'**Relevance score**: {paper["score"]}/10  \n')
        f.write(f'**Authors**: {", ".join(paper["authors"])}  \n')
        f.write(f'**Link**: {paper["link"]}\n\n')

        summary = summarize_paper(paper['abstract'])
        f.write(summary)

        f.write('\n\n---\n\n')
        time.sleep(2)

    f.write("## Filtered Out (lowest 5 scores)\n\n")
    for paper in papers[-5:]:
        f.write(f"- [{paper['score']}/10] {paper['title']}\n")

print(f"Digest saved to {filename}")

with open(filename, 'r', encoding='utf-8') as f:
    digest_content = f.read()

send_digest_email(digest_content, f"AI Research Digest: {today}")