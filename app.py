import streamlit as st
from pathlib import Path
import os
from dotenv import load_dotenv
from data_loader import DataLoader
from rag_engine import RAGEngine
import config

load_dotenv()

st.set_page_config(
    page_title="YC Startup Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .main { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    
    h1 {
        background: linear-gradient(135deg, #FF6600 0%, #FF8C42 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
    }
    
    .stChatMessage {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #FF6600 0%, #FF8C42 100%);
        color: white;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(255, 102, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 102, 0, 0.4);
    }
    
    .source-box {
        background: #f8f9fa;
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 4px solid #FF6600;
        margin: 0.8rem 0;
    }
    
    .reasoning-step {
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-left: 3px solid #667eea;
        background: #f8f9fa;
        border-radius: 8px;
    }
    
    .confidence-badge {
        background: linear-gradient(135deg, #FF6600 0%, #FF8C42 100%);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(255, 102, 0, 0.3);
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'rag_engine' not in st.session_state:
        st.session_state.rag_engine = None
    if 'use_fast_model' not in st.session_state:
        st.session_state.use_fast_model = True

def setup_sidebar():
    with st.sidebar:
        st.title("⚙️ Settings")
        st.markdown("---")
        
        st.subheader("🎯 Model Selection")
        use_pro = st.toggle(
            "Use Pro Mode",
            value=not st.session_state.use_fast_model,
            help="Toggle ON for Gemini 2.5 Pro (best quality) or OFF for Flash (faster)"
        )
        st.session_state.use_fast_model = not use_pro
        
        if use_pro:
            st.success("🚀 Gemini 2.5 Pro - Best Quality")
        else:
            st.info("⚡ Gemini 2.5 Flash - Fast Responses")
        
        st.markdown("---")
        st.subheader("💡 Example Questions")
        for query in config.EXAMPLE_QUERIES:
            if st.button(query, key=query, use_container_width=True):
                st.session_state.example_query = query
        
        st.markdown("---")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("""
        ### 📚 Knowledge Base
        - 40+ Paul Graham Essays
        - YC Startup Wisdom
        - Founder Best Practices
        """)

def load_rag_engine():
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        st.error("⚠️ GOOGLE_API_KEY not found in .env file")
        return None
    
    if st.session_state.rag_engine is None or st.session_state.get('last_model') != st.session_state.use_fast_model:
        vectorstore_path = 'data/processed/vectorstore'
        
        if not Path(vectorstore_path).exists():
            st.error("⚠️ Knowledge base not found. Run: `python data_loader.py`")
            return None
        
        with st.spinner("🔄 Loading..."):
            try:
                loader = DataLoader(api_key)
                vectorstore = loader.load_vectorstore(vectorstore_path)
                st.session_state.rag_engine = RAGEngine(
                    vectorstore, 
                    api_key, 
                    use_fast_model=st.session_state.use_fast_model
                )
                st.session_state.last_model = st.session_state.use_fast_model
                return st.session_state.rag_engine
            except Exception as e:
                st.error(f"❌ Error: {e}")
                return None
    
    return st.session_state.rag_engine

def main():
    load_custom_css()
    initialize_session_state()
    
    st.title("🚀 YC Startup Assistant")
    st.markdown("<p style='text-align: center; color: #666; font-size: 1.1rem;'>Your AI-powered advisor trained on Y Combinator wisdom</p>", unsafe_allow_html=True)
    
    setup_sidebar()
    
    rag_engine = load_rag_engine()
    if not rag_engine:
        return
    
    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])
            if msg.get('sources'):
                st.markdown("**📚 Sources:**")
                for src in msg['sources']:
                    st.markdown(f"""<div class='source-box'><strong>{src['title']}</strong><br>
                    <a href="{src['url']}" target="_blank">📖 Read essay →</a></div>""", unsafe_allow_html=True)
            if msg.get('confidence'):
                st.markdown(f"<div class='confidence-badge'>⭐ {msg['confidence']:.0f}%</div>", unsafe_allow_html=True)
    
    prompt = st.session_state.pop('example_query', None) or st.chat_input("💬 Ask anything about startups...")
    
    if prompt:
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    result = rag_engine.query(prompt)
                    st.markdown(result['answer'])
                    
                    if result.get('sources'):
                        st.markdown("**📚 Sources:**")
                        for src in result['sources']:
                            st.markdown(f"""<div class='source-box'><strong>{src['title']}</strong><br>
                            <a href="{src['url']}" target="_blank">📖 Read essay →</a></div>""", unsafe_allow_html=True)
                    
                    if result.get('confidence'):
                        st.markdown(f"<div class='confidence-badge'>⭐ Confidence: {result['confidence']:.0f}%</div>", unsafe_allow_html=True)
                    
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': result['answer'],
                        'sources': result.get('sources'),
                        'confidence': result.get('confidence')
                    })
                except Exception as e:
                    st.error(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
