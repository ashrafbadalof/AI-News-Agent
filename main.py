import time
from src.fetch_arxiv import fetch_arxiv
from src.summarize import summarize_paper

url = 'http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=10'

papers = fetch_arxiv(url=url)
# print(len(papers), "papers fetched")

for paper in papers:
    print(f'## {paper["title"]}\n')
    print(f'Authors: {", ".join(paper["authors"])}')
    print(f'Link: {paper["link"]}\n')

    summary = summarize_paper(paper['abstract'])
    print(summary)

    print('\n' + '='*50 + '\n')
    time.sleep(2)