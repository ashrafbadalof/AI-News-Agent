import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

SUMMARY_PROMPT = """Summarize the following abstract by specifying Problem, Approach, Key Result, Why it matters and Background to know in an easy way. Do not include a title or any preamble. Start directly with ## Problem. 
Use exactly these five headers, identical wording each time: ## Problem, ## Approach, ## Key Result, ## Why It Matters, ## Background to Know (List 2-3 technical concepts a reader should be familiar with to understand this paper. Just the term names as bullet 
points, no explanations.). No bold inside headers. Each section should be 1 to 3 sentences. Total summary under 200 words. 
Use bullets only when there are 3+ distinct items to list. Otherwise prefer prose. Start summarization right away, do not include anything not related to the abstract. Explain technical terms briefly when they are central to understanding the approach 

Abstract:
{abstract}"""

def summarize_paper(abstract:str) -> str:
    response = client.messages.create(
        model='claude-haiku-4-5',
        max_tokens=1000,
        messages=[{'role': 'user', 'content': SUMMARY_PROMPT.format(abstract = abstract)} ]
        )
    return response.content[0].text
