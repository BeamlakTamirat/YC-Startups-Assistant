# 🚀 YC Startup Assistant

An AI-powered startup advisor trained on Y Combinator wisdom, Paul Graham's essays, and startup best practices. Get actionable advice for your startup journey.

![YC Startup Assistant](https://img.shields.io/badge/Built%20with-LangChain-blue) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-red) ![Python](https://img.shields.io/badge/Python-3.9+-green)

## 🎯 What It Does

This RAG-powered assistant helps founders by:
- Answering startup questions using YC knowledge base
- Providing specific, actionable advice from Paul Graham's essays
- Showing reasoning steps for transparency
- Citing sources for every answer
- Calculating confidence scores for responses

## ✨ Features

- **Smart Retrieval**: Semantic search across 40+ Paul Graham essays
- **ReAct Reasoning**: Shows step-by-step thinking process
- **Source Citations**: Every answer includes essay references with links
- **Confidence Scoring**: Know how certain the AI is about its answer
- **Beautiful UI**: Clean, YC-branded interface
- **Chat Memory**: Maintains conversation context

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get FREE Google API Key

Visit [aistudio.google.com/apikey](https://aistudio.google.com/apikey) and create a free API key.

### 3. Set Up Knowledge Base

First, scrape Paul Graham's essays:

```bash
python utils/scraper.py
```

Then build the vector database:

```bash
export GOOGLE_API_KEY='your-key-here'
python data_loader.py
```

### 4. Run the App

```bash
streamlit run app.py
```

Enter your Google API key in the sidebar and start asking questions!

## 💡 Example Questions

- "How do I validate my startup idea before building?"
- "What should I look for in a co-founder?"
- "When is the right time to raise funding vs bootstrap?"
- "How do I get my first 100 users?"
- "What are signs of product-market fit?"

## 🏗️ Architecture

```
User Query
    ↓
Streamlit UI
    ↓
RAG Engine (LangChain)
    ↓
FAISS Vector Store → Retrieve relevant chunks
    ↓
Google Gemini 2.5 Pro/Flash → Generate answer
    ↓
Response + Sources + Confidence
```

## 📁 Project Structure

```
yc-startup-assistant/
├── app.py                 # Streamlit UI
├── rag_engine.py          # RAG logic
├── data_loader.py         # Data processing
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── utils/
│   └── scraper.py        # Essay scraper
└── data/
    ├── raw/              # Scraped essays
    └── processed/        # Vector store
```

## 🛠️ Tech Stack

- **LangChain**: RAG orchestration
- **FAISS**: Vector database
- **Google Gemini 2.0 Flash**: LLM (FREE)
- **Google Embeddings**: Text embeddings (FREE)
- **Streamlit**: Web interface
- **BeautifulSoup**: Web scraping

## 🌐 Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Deploy!

Users will enter their own Google API keys via the UI (completely FREE).


