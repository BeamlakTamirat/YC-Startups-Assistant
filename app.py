import streamlit as st
from pathlib import Path
import sys
from data_loader import DataLoader
from rag_engine import RAGEngine
import config

st.set_page_config(
    page_title="YC Startup Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_custom_css():
    st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stButton>button {
        background-color: #FF6600;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #E55A00;
    }
    .source-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FF6600;
        margin: 0.5rem 0;
    }
    .reasoning-step {
        color: #666;
        font-size: 0.9rem;
        padding: 0.3rem 0;
    }
    .confidence-score {
        background-color: #FF6600;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: 600;
        display: inline-block;
    }
    h1 {
        color: #FF6600;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'rag_engine' not in st.session_state:
        st.session_state.rag_engine = None
    if 'vectorstore' not in st.session_state:
        st.session_state.vectorstore = None
    if 'use_fast_model' not in st.session_state:
        st.session_state.use_fast_model = False

def setup_sidebar():
    with st.sidebar:
        st.title("⚙️ Settings")
        
        api_key = st.text_input(
            "Google API Key",
            type="password",
            help="Enter your Google API key to use the assistant"
        )
        
        if api_key:
            st.session_state.api_key = api_key
        
        st.markdown("---")
        
        st.subheader("🚀 Model Selection")
        use_fast = st.toggle(
            "Use Fast Mode (2.5 Flash)",
            value=st.session_state.use_fast_model,
            help="Toggle between Gemini 2.5 Pro (best quality) and 2.5 Flash (faster responses)"
        )
        if use_fast != st.session_state.use_fast_model:
            st.session_state.use_fast_model = use_fast
            st.session_state.rag_engine = None
        
        st.markdown("---")
        
        st.subheader("💡 Example Questions")
        for query in config.EXAMPLE_QUERIES:
            if st.button(query, key=query, use_container_width=True):
                st.session_state.example_query = query
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("""
        ### About
        This assistant is trained on:
        - Paul Graham's Essays
        - Y Combinator Wisdom
        - Startup Best Practices
        
        Built with Gemini 2.5 Pro/Flash (FREE)
        LangChain & Streamlit
        """)

def load_rag_engine(api_key):
    if st.session_state.rag_engine is None:
        vectorstore_path = 'data/processed/vectorstore'
        
        if not Path(vectorstore_path).exists():
            st.error("⚠️ Knowledge base not found. Please run data setup first.")
            st.info("Run: `python data_loader.py` to build the knowledge base")
            return None
        
        with st.spinner("Loading knowledge base..."):
            try:
                loader = DataLoader(api_key)
                vectorstore = loader.load_vectorstore(vectorstore_path)
                st.session_state.vectorstore = vectorstore
                st.session_state.rag_engine = RAGEngine(
                    vectorstore, 
                    api_key, 
                    use_fast_model=st.session_state.use_fast_model
                )
                return st.session_state.rag_engine
            except Exception as e:
                st.error(f"Error loading knowledge base: {e}")
                return None
    
    return st.session_state.rag_engine

def display_message(role, content, sources=None, confidence=None, reasoning=None):
    with st.chat_message(role):
        st.markdown(content)
        
        if reasoning:
            with st.expander("💭 How I thought about this"):
                for step in reasoning:
                    st.markdown(f"<div class='reasoning-step'>{step}</div>", unsafe_allow_html=True)
        
        if sources:
            st.markdown("**📚 Sources:**")
            for source in sources:
                st.markdown(f"""
                <div class='source-box'>
                    <strong>{source['title']}</strong><br>
                    <a href="{source['url']}" target="_blank">Read full essay →</a>
                </div>
                """, unsafe_allow_html=True)
        
        if confidence:
            st.markdown(f"<span class='confidence-score'>⭐ Confidence: {confidence:.0f}%</span>", unsafe_allow_html=True)

def main():
    load_custom_css()
    initialize_session_state()
    
    st.title("🚀 YC Startups Assistant")
    st.markdown("*Your AI advisor trained on Y Combinator wisdom*")
    
    setup_sidebar()
    
    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.warning("👈 Please enter your Google API key in the sidebar to get started")
        st.info("Don't have an API key? Get one FREE at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)")
        return
    
    rag_engine = load_rag_engine(st.session_state.api_key)
    
    if not rag_engine:
        return
    
    for message in st.session_state.messages:
        display_message(
            message['role'],
            message['content'],
            message.get('sources'),
            message.get('confidence'),
            message.get('reasoning')
        )
    
    if 'example_query' in st.session_state:
        prompt = st.session_state.example_query
        del st.session_state.example_query
    else:
        prompt = st.chat_input("Ask me anything about startups...")
    
    if prompt:
        st.session_state.messages.append({
            'role': 'user',
            'content': prompt
        })
        
        display_message('user', prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = rag_engine.query(prompt)
                    
                    st.markdown(result['answer'])
                    
                    if result['reasoning_steps']:
                        with st.expander("💭 How I thought about this"):
                            for step in result['reasoning_steps']:
                                st.markdown(f"<div class='reasoning-step'>{step}</div>", unsafe_allow_html=True)
                    
                    if result['sources']:
                        st.markdown("**📚 Sources:**")
                        for source in result['sources']:
                            st.markdown(f"""
                            <div class='source-box'>
                                <strong>{source['title']}</strong><br>
                                <a href="{source['url']}" target="_blank">Read full essay →</a>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    if result['confidence']:
                        st.markdown(f"<span class='confidence-score'>⭐ Confidence: {result['confidence']:.0f}%</span>", unsafe_allow_html=True)
                    
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': result['answer'],
                        'sources': result['sources'],
                        'confidence': result['confidence'],
                        'reasoning': result['reasoning_steps']
                    })
                
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.info("Please check your API key and try again.")

if __name__ == "__main__":
    main()
    
