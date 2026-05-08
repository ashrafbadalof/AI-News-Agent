import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

RELEVANCE_PROMPT = """You are filtering arXiv papers for a reader with this profile:

The reader is a Master's student in AI heading toward an industry role. They have solid foundations in machine learning, NLP, neural networks (transformers, attention, embeddings), and computer vision. They have NOT taken a reinforcement learning course, so papers requiring fluency in RL algorithms, policy optimisation methods (PPO, GRPO, etc.), or reward shaping techniques are less accessible to them. They prefer papers where the contribution is clearly motivated and the practical implications are explained.

The reader is interested in:
- Practical applications of large language models in real systems
- LLM agents, tool use, and how models orchestrate tasks (conceptual treatments preferred over deep RL methodology)
- Retrieval-augmented generation (RAG), search, and information retrieval with LLMs
- Fine-tuning, prompting, and evaluation of language models
- Multimodal models combining language and vision
- Deployment-focused work: inference efficiency, serving, scaling, latency, cost
- Survey papers and accessible introductions to new areas
- Applied papers where someone built something and reports what worked
- Papers that USE reinforcement learning to build or improve LLM agents and reasoning systems, where RL is the means rather than the contribution
- Comparative or analytical papers that explain how RL training affects language models (these often teach RL concepts as a side effect)

The reader is less interested in:
- Pure RL methodology papers where the contribution is a new algorithm or algorithmic variant (e.g., novel optimisation methods, modifications to PPO/GRPO/DPO/etc., reward modelling techniques) — these require fluent RL background to appreciate- Highly theoretical work without clear applied motivation
- Domain-specific medical, biological, or physics applications unless the method is generally useful
- Pure mathematical or optimisation contributions
- Papers that assume deep familiarity with a narrow subfield without accessible motivation

Rate the following paper's relevance to the reader on a scale of 1 to 10, where:
- 10 = exactly what they want to read
- 5 = adjacent but maybe interesting
- 1 = completely irrelevant to their interests

Output ONLY a single integer between 1 and 10. No explanation, no other text.

Title: {title}
Abstract: {abstract}"""

def rate_relevance(paper: dict) -> int:
    response = client.messages.create(
        model='claude-haiku-4-5',
        max_tokens=10,
        messages=[
            {'role':'user', 'content':RELEVANCE_PROMPT.format(
                title = paper['title'],
                abstract = paper['abstract']   
            )}
        ]
    )

    text = response.content[0].text.strip()
    try:
        return int(text)
    except ValueError:
        return 5