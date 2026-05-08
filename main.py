import time
from src.fetch_arxiv import fetch_arxiv
from src.summarize import summarize_paper
from src.relevance import rate_relevance

url = 'http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=30'

papers = fetch_arxiv(url=url)
# print(len(papers), "papers fetched")
for paper in papers:
    paper['score'] = rate_relevance(paper)
    time.sleep(0.5)

papers.sort(key=lambda p: p['score'], reverse=True)
top_papers = papers[:5]

for paper in top_papers:
    print(f'## {paper["title"]}')
    print(f'Relevance score: {paper["score"]}/10')
    print(f'Authors: {", ".join(paper["authors"])}')
    print(f'Link: {paper["link"]}\n')

    summary = summarize_paper(paper['abstract'])
    print(summary)

    print('\n' + '='*50 + '\n')
    time.sleep(2)

print("--- FILTERED OUT (bottom 5) ---")
for paper in papers[-5:]:
    print(f"[{paper['score']}/10] {paper['title']}")