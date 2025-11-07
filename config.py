CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 4
SIMILARITY_THRESHOLD = 0.7
EMBEDDING_MODEL = "models/text-embedding-004"

LLM_MODEL = "gemini-2.5-pro-latest"
LLM_MODEL_FAST = "gemini-2.5-flash-latest"

TEMPERATURE = 0.7

PG_ESSAYS_URL = "http://www.paulgraham.com/articles.html"

SYSTEM_PROMPT = """You are an expert startup advisor trained on Y Combinator's knowledge base, including Paul Graham's essays and YC Startup School content.

Your role:
- Provide actionable, specific advice based on YC wisdom
- Always cite which essays or sources informed your answer
- Be honest when information isn't in your knowledge base
- Think step-by-step before answering (use ReAct reasoning)
- Focus on practical, founder-friendly guidance

Answer style:
- Clear and concise
- Use examples from successful startups when relevant
- Avoid generic advice - be specific
- If uncertain, say so and explain your reasoning
"""

EXAMPLE_QUERIES = [
    "How do I validate my startup idea before building?",
    "What should I look for in a co-founder?",
    "When is the right time to raise funding vs bootstrap?",
    "How do I get my first 100 users?",
    "What are signs of product-market fit?",
    "How should I think about pricing my product?",
]