from src.fetch_arxiv import fetch_arxiv

url = 'http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=10'

papers = fetch_arxiv(url=url)
print(len(papers), "papers fetched")

for paper in papers:
    print(", ".join(paper['authors']))
    print(paper['link'])
    print(paper['title'])
    print(paper['abstract'], '\n')