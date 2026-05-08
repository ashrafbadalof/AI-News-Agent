import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

SUMMARY_PROMPT = """Summarize the following abstract by specifying Problem, Approach, Key Result and Why it matters in an easy way. Do not include a title or any preamble. Start directly with ## Problem. 
Use exactly these four headers, identical wording each time: ## Problem, ## Approach, ## Key Result, ## Why It Matters. No bold inside headers. Each section should be 1 to 3 sentences. Total summary under 200 words. 
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
