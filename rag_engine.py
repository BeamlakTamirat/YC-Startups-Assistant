from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
import config

class ReasoningCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.steps = []
    
    def on_chain_start(self, serialized, inputs, **kwargs):
        self.steps.append("🔍 Analyzing query...")
    
    def on_retriever_start(self, serialized, query, **kwargs):
        self.steps.append("📚 Searching knowledge base...")
    
    def on_retriever_end(self, documents, **kwargs):
        self.steps.append(f"✓ Found {len(documents)} relevant sources")

class RAGEngine:
    def __init__(self, vectorstore, google_api_key, use_fast_model=False):
        self.vectorstore = vectorstore
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            google_api_key=google_api_key
        )
        model = config.LLM_MODEL_FAST if use_fast_model else config.LLM_MODEL
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=config.TEMPERATURE,
            google_api_key=google_api_key
        )
        self.retriever = vectorstore.as_retriever(
            search_kwargs={"k": config.TOP_K_RESULTS}
        )
        self._setup_chain()
    
    def _setup_chain(self):
        prompt_template = """You are an expert startup advisor trained on Y Combinator wisdom.

Context from knowledge base:
{context}

Question: {question}

Instructions:
1. Think step-by-step about the question
2. Use the context above to provide specific, actionable advice
3. Cite which essays/sources you're drawing from
4. If the context doesn't contain relevant information, say so honestly

Answer:"""

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
    
    def get_reasoning_steps(self, query):
        """Generate reasoning steps for transparency"""
        steps = [
            "🤔 Understanding your question...",
            "🔍 Searching YC knowledge base...",
            "📊 Analyzing relevant essays...",
            "💡 Synthesizing answer..."
        ]
        return steps
    
    def calculate_confidence(self, source_docs):
        if not source_docs:
            return 0.0
        
        return min(len(source_docs) / config.TOP_K_RESULTS * 100, 95)
    
    def format_sources(self, source_docs):
        sources = []
        seen_titles = set()
        
        for doc in source_docs:
            title = doc.metadata.get('title', 'Unknown')
            if title not in seen_titles:
                sources.append({
                    'title': title,
                    'url': doc.metadata.get('url', ''),
                    'source': doc.metadata.get('source', 'YC Knowledge Base')
                })
                seen_titles.add(title)
        
        return sources
    
    def query(self, question):
        reasoning_steps = self.get_reasoning_steps(question)
        
        result = self.qa_chain.invoke({"query": question})
        
        answer = result['result']
        source_docs = result['source_documents']
        
        sources = self.format_sources(source_docs)
        confidence = self.calculate_confidence(source_docs)
        
        return {
            'answer': answer,
            'sources': sources,
            'confidence': confidence,
            'reasoning_steps': reasoning_steps
        }
    
    def stream_query(self, question, callback=None):
        reasoning_steps = self.get_reasoning_steps(question)
        
        source_docs = self.retriever.get_relevant_documents(question)
        
        context = "\n\n".join([doc.page_content for doc in source_docs[:config.TOP_K_RESULTS]])
        
        prompt = f"""{config.SYSTEM_PROMPT}

Context from knowledge base:
{context}

Question: {question}

Provide a detailed, actionable answer based on the context above. Cite specific essays when relevant."""

        sources = self.format_sources(source_docs)
        confidence = self.calculate_confidence(source_docs)
        
        return {
            'prompt': prompt,
            'sources': sources,
            'confidence': confidence,
            'reasoning_steps': reasoning_steps,
            'source_docs': source_docs
        }

