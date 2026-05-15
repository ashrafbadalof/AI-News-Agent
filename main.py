import time
import logging
from src.fetch_arxiv import fetch_arxiv
from src.summarize import summarize_paper
from src.relevance import rate_relevance
from src.email_sender import send_digest_email
from src.fetch_huggingface import fetch_huggingface

from datetime import datetime
from pathlib import Path

from config import ARXIV_MAX_RESULTS, ARXIV_CATEGORIES, HF_MAX_RESULTS, TOP_N_PAPERS

def extract_arxiv_id(link):
    try:
        id_part = link.split('/abs/')[-1]
        return id_part.split('v')[0]
    except:
        return None

Path('digests').mkdir(exist_ok=True)

log_file = Path("digests") / "log.txt"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)

today = datetime.now().strftime("%Y-%m-%d")
filename = f"digests/digest_{today}.md"

logging.info(f'Starting digest run for {today}')

try:
    hf_papers = fetch_huggingface(HF_MAX_RESULTS)
    logging.info(f'Fetched {len(hf_papers)} HF papers')
except Exception as e:
    logging.error(f'HF fetch failed {e}')
    hf_papers = []

category_query = "+OR+".join(f"cat:{c}" for c in ARXIV_CATEGORIES)
try:
    url = (f"http://export.arxiv.org/api/query?"
           f"search_query={category_query}"
           f"&sortBy=submittedDate&sortOrder=descending"
           f"&max_results={ARXIV_MAX_RESULTS}")
    papers = fetch_arxiv(url=url)
    logging.info(f'Fetched {len(papers)} arXiv papers')
except Exception as e:
    logging.error(f'arXiv fetch failed {e}')
    papers = []

top_papers = []
if papers:
    logging.info('Scoring relevance')
    for paper in papers:
        paper['score'] = rate_relevance(paper)
        time.sleep(0.5)
    papers.sort(key=lambda p: p['score'], reverse=True)
    top_papers = papers[:TOP_N_PAPERS]
    logging.info(f'Top scores: {[p["score"] for p in top_papers]}')

arxiv_ids = set()
for paper in top_papers:
    a_id = extract_arxiv_id(paper['link'])
    if a_id:
        arxiv_ids.add(a_id)

hf_papers_before = len(hf_papers)
hf_papers = [
    p for p in hf_papers 
    if extract_arxiv_id(p['link']) not in arxiv_ids
]
removed = hf_papers_before - len(hf_papers)
if removed > 0:
    logging.info(f"Removed {removed} duplicate HF papers")

with open(filename, 'w', encoding='utf-8') as f:
    f.write(f'# AI Research Digest {today}\n\n')
    
    if top_papers:
        f.write("## arXiv Papers\n\n")
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
    else:
        f.write('## arXiv Papers\n\n arXiv fetch failed today. Check log for details \n\n---\n\n')
    
    if hf_papers:
        f.write("## HF Daily Papers (community picks)\n\n")
        for paper in hf_papers:
            f.write(f"- **[{paper['upvotes']} upvotes]** [{paper['title']}]({paper['link']}) — {paper['ai_summary']}\n")
        f.write("\n---\n\n")
    else:
        f.write('## HF Daily Papers \n\n HF fetch failed today. Check log for details \n\n---\n\n')

    if papers:
        f.write("## Filtered Out (lowest 5 scores)\n\n")
        for paper in papers[-5:]:
            f.write(f"- [{paper['score']}/10] {paper['title']}\n")

logging.info(f"Digest saved to {filename}")

try:
    with open(filename, 'r', encoding='utf-8') as f:
        digest_content = f.read()
    send_digest_email(digest_content, f"AI Research Digest: {today}")
    logging.info('Email sent successfully')
except Exception as e:
    logging.error(f'Email failed: {e}')

logging.info("Run complete\n")