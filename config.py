CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 4
SIMILARITY_THRESHOLD = 0.7
EMBEDDING_MODEL = "models/text-embedding-004"

LLM_MODEL = "gemini-2.5-pro"
LLM_MODEL_FAST = "gemini-2.5-flash-lite"

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
    "🚀 How do I find product-market fit for my startup?",
    "💡 What makes a great startup idea vs a bad one?",
    "👥 Should I build alone or find a co-founder first?",
    "💰 When should I raise VC funding vs bootstrap?",
    "📈 How do I get my first 1,000 users without paid ads?",
    "🎯 What should I focus on in the first 3 months?",
    "💹 How do I know if my startup is growing fast enough?",
    "🔥 What are the biggest mistakes first-time founders make?",
]