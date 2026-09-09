# Groundwater Assistant Chatbot

A hybrid chatbot that answers groundwater-related questions by combining structured data lookups (state/block-level CSV data) with semantic search + LLM reasoning (RAG using FAISS and Google Gemini) for conceptual questions.

## 🚀 Live Demo

**Try the chatbot here:**
https://groundwater-chatbot-nc6enn9p7tk2dvynptsfwe.streamlit.app/

## 📌 Overview

This project answers questions about groundwater conditions across Indian states and blocks — such as extraction levels, rainfall, recharge, and categorization (**Safe / Semi-Critical / Critical / Over-Exploited**) — using two complementary approaches:

### 1. Direct Data Queries

For structured, factual questions such as:

> "How many states are over-exploited in 2019?"

The chatbot filters and aggregates data directly from CSV files to provide fast and precise answers.

### 2. RAG-Based Conceptual Answers

For open-ended or explanatory questions such as:

> "Why is over-exploitation a concern?"

The chatbot retrieves relevant context using a FAISS vector index built with Sentence Transformers, then generates a grounded response using Google's Gemini model.

## ✨ Features

* 📊 **State-level reports** — rainfall, recharge, extraction, and stage-of-extraction summaries per state and year.
* 📍 **Block-level lookups** — detailed groundwater statistics for a specific block/district.
* 🔍 **Category-based filtering** — find states/blocks categorized as Safe, Semi-Critical, Critical, or Over-Exploited for a given year.
* 🤖 **Conceptual Q&A** — natural-language explanations powered by Gemini and grounded using retrieved context through FAISS.
* 🌐 **Web interface** — interactive chatbot interface built with Streamlit.

## 🛠️ Tech Stack

* **Python**
* **Pandas / NumPy** — data processing and manipulation
* **Sentence Transformers (`all-MiniLM-L6-v2`)** — text embeddings
* **FAISS** — vector similarity search
* **Google Generative AI (`gemini-2.5-flash`)** — LLM response generation
* **FastAPI** — backend/API serving
* **Streamlit** — web interface

## 📂 Project Structure

```text
.
├── app.py                # Main application entry point / web server
├── ui.py                 # UI rendering logic
├── chatbot.py            # Core chatbot logic (RAG + structured query handling)
├── block_data.csv        # Block-level groundwater data
├── block_data.txt        # Block-level text documents for embedding/retrieval
├── state_data.csv        # State-level groundwater data
├── state_data.txt        # State-level text documents for embedding/retrieval
├── public/fonts/         # Font assets for the UI
├── requirements.txt      # Python dependencies
└── .gitignore
```

## ⚙️ Setup

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

The chatbot requires a Google Generative AI API key.

**macOS/Linux:**

```bash
export GOOGLE_API_KEY="your_api_key_here"
```

**Windows:**

```bash
setx GOOGLE_API_KEY "your_api_key_here"
```

### 4. Run the application

```bash
python app.py
```

## 💬 Usage Examples

The chatbot supports both structured and conceptual queries.

### Structured Queries

```python
chatbot_api("How many states are over exploited in 2019?")

chatbot_api("Which state is over exploited in 2019?")

chatbot_api("What is the groundwater condition in Bihar in 2019?")

chatbot_api("In 2019, what was the groundwater status of Bawani Khera block in Haryana?")
```

### Conceptual Queries

```python
chatbot_api("Why is over-exploitation of groundwater a concern?")
```

## 🔄 How It Works

### 1. Data Loading

Block-level and state-level datasets are loaded from CSV files and normalized by cleaning formatting and standardizing category names.

### 2. Embedding & Vector Indexing

Text documents from `block_data.txt` and `state_data.txt` are converted into vector embeddings using the `all-MiniLM-L6-v2` Sentence Transformer model.

These embeddings are stored in a **FAISS vector index** for efficient semantic similarity search.

### 3. Query Routing

Incoming questions are routed based on their intent:

* **Conceptual queries** containing terms such as `why`, `impact`, `concern`, `explain`, or `effect` → **RAG + Gemini pipeline**
* **Structured queries** involving `state`, `block`, `category`, `year`, etc. → **Direct Pandas/CSV data retrieval**

### 4. Response Generation

For structured queries, the system performs filtering and aggregation directly on the CSV datasets.

For conceptual queries, the system:

1. Converts the query into an embedding.
2. Searches the FAISS index for relevant context.
3. Retrieves the top-k relevant chunks.
4. Passes the retrieved context to Gemini.
5. Generates a grounded natural-language response.

## 🧠 Hybrid Architecture

```text
                    User Query
                        │
                        ▼
                 Query Router
                  /           \
                 /             \
        Structured Query    Conceptual Query
              │                    │
              ▼                    ▼
       CSV / Pandas           Sentence Transformer
        Data Lookup                  │
              │                      ▼
              │                  FAISS Search
              │                      │
              │                      ▼
              │              Relevant Context
              │                      │
              │                      ▼
              │                  Gemini LLM
              │                      │
              └──────────┬───────────┘
                         ▼
                    Final Response
```

## 🛡️ Error Handling

If the Gemini API rate limit is reached, the chatbot gracefully handles the failure and provides a message asking the user to retry or use a data-based query.

Category names are normalized to ensure consistent filtering. For example:

```text
over-exploited
over_exploited
over exploited
```

are normalized to:

```text
over exploited
```

## 📈 Future Improvements

* Improve query routing using an intent-classification model instead of keyword-based routing.
* Add conversation memory for multi-turn questions.
* Improve retrieval using metadata filtering and hybrid search.
* Add evaluation metrics for RAG retrieval and answer quality.
* Add support for more groundwater datasets and years.
* Containerize the application using Docker for easier deployment.

## 📄 License

Add your license here.
