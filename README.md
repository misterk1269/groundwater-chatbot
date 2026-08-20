# Groundwater Assistant Chatbot

A hybrid chatbot that answers groundwater-related questions by combining **structured data lookups** (state/block level CSV data) with **semantic search + LLM reasoning** (RAG using FAISS and Google Gemini) for conceptual questions.

## Overview

This project answers questions about groundwater conditions across Indian states and blocks — such as extraction levels, rainfall, recharge, and categorization (Safe / Semi-Critical / Critical / Over-Exploited) — using two complementary approaches:

1. **Direct data queries** — For structured, factual questions (e.g. *"How many states are over-exploited in 2019?"*), the chatbot filters and aggregates data directly from CSV files for fast, precise answers.
2. **RAG-based conceptual answers** — For open-ended or explanatory questions (e.g. *"Why is over-exploitation a concern?"*), the chatbot retrieves relevant context using a FAISS vector index built with Sentence Transformers, then generates an answer using Google's Gemini model.

## Features

- 📊 **State-level reports** — rainfall, recharge, extraction, and stage-of-extraction summaries per state and year.
- 📍 **Block-level lookups** — detailed groundwater stats for a specific block/district.
- 🔍 **Category-based filtering** — find all states/blocks marked Safe, Semi-Critical, Critical, or Over-Exploited for a given year.
- 🤖 **Conceptual Q&A** — natural language explanations powered by Gemini, grounded in retrieved context via FAISS semantic search.
- 🌐 **Web interface** — served via `app.py` / `ui.py`.

## Tech Stack

- **Python**
- [Sentence Transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`) — text embeddings
- [FAISS](https://github.com/facebookresearch/faiss) — vector similarity search
- [Google Generative AI](https://ai.google.dev/) (`gemini-2.5-flash`) — LLM responses
- **Pandas / NumPy** — data processing
- FastAPI (via `app.py`) — web serving

## Project Structure

```
.
├── app.py                # Main application entry point / web server
├── ui.py                 # UI rendering logic
├── chatbot.py             # Core chatbot logic (RAG + structured query handling)
├── block_data.csv         # Block-level groundwater data
├── block_data.txt         # Block-level text documents for embedding/retrieval
├── state_data.csv         # State-level groundwater data
├── state_data.txt         # State-level text documents for embedding/retrieval
├── public/fonts/          # Font assets for the UI
├── requirements.txt       # Python dependencies
└── .gitignore
```

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd <repo-folder>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your Gemini API key

The chatbot requires a Google Generative AI API key, set as an environment variable:

```bash
export GOOGLE_API_KEY="your_api_key_here"      # macOS/Linux
setx GOOGLE_API_KEY "your_api_key_here"        # Windows
```

### 4. Run the app

```bash
python app.py
```

## Usage Examples

The chatbot understands both structured and conceptual queries:

```python
chatbot_api("How many states are over exploited in 2019?")
chatbot_api("Which state is over exploited in 2019?")
chatbot_api("What is the groundwater condition in Bihar in 2019?")
chatbot_api("In 2019, what was the groundwater status of Bawani Khera block in Haryana?")
chatbot_api("Why is over-exploitation of groundwater a concern?")
```

## How It Works

1. **Data Loading** — Block and state-level data are loaded from CSV files and normalized (lowercased categories, cleaned formatting).
2. **Embedding Index** — Text documents (`block_data.txt`, `state_data.txt`) are embedded using `all-MiniLM-L6-v2` and indexed with FAISS for similarity search.
3. **Query Routing** — Incoming questions are classified:
   - Conceptual keywords (*why, impact, concern, explain, effect*) → routed to the **RAG + Gemini** pipeline.
   - Structured keywords (*state, block, category, year*) → routed to **direct pandas filtering** on the CSV data.
4. **Response Generation** — Structured queries return formatted summaries; conceptual queries retrieve top-k relevant context chunks and pass them to Gemini for a grounded natural language response.

## Notes

- If the Gemini API rate limit is hit, the chatbot gracefully falls back to a message asking the user to retry or ask a data-based query instead.
- Category names are normalized (e.g. `over-exploited`, `over_exploited` → `over exploited`) to ensure consistent filtering.

## License

Add your license here.
