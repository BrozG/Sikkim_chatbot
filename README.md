# 🏔️ Sikkim AI Chatbot

> An AI-powered chatbot for tourists visiting Sikkim, built with LangChain, WatsonX LLM, and a RAG pipeline trained on real Sikkim government documents and historical books.

---

## ✨ Features

- 🗺️ Answers questions about **Sikkim tourism, history, and taxi fares**
- 📄 Trained on **real government PDFs** — official Sikkim taxi fare charts and historical books
- 🔍 **RAG pipeline** — retrieves relevant context from vector store before answering
- 🔄 **Auto-detects new PDFs** — uses file hash detection to update vector store when new data is added
- 💬 Simple **Streamlit UI** for easy interaction
- ⚡ Powered by **IBM WatsonX LLM**

---

## 🧠 How It Works

```
User Question
      ↓
┌─────────────────────────┐
│   Hash Check            │  ← Detects if new PDFs added to /data
│   Auto-update Vector    │  ← Rebuilds vector store if changed
└─────────────────────────┘
      ↓
┌─────────────────────────┐
│   Vector Store Lookup   │  ← Finds relevant chunks from PDFs
│   (FAISS)               │
└─────────────────────────┘
      ↓
┌─────────────────────────┐
│   WatsonX LLM           │  ← Generates answer with context
│   (Sikkim prompt)       │
└─────────────────────────┘
      ↓
   Answer to User
```

---

## 📚 Data Sources

| Source | Content |
|---|---|
| Government PDFs | Official Sikkim taxi fare charts |
| Historical Books | History and culture of Sikkim |

> Just drop new PDFs into the `data/` folder — the chatbot auto-detects and updates! 🔄

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | IBM WatsonX |
| RAG Pipeline | LangChain |
| Vector Store | FAISS |
| Embeddings | HuggingFace |
| UI | Streamlit |
| Language | Python |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/BrozG/Sikkim_chatbot
cd Sikkim_chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file:
```bash
WATSONX_API_KEY="your_watsonx_api_key"
WATSONX_PROJECT_ID="your_project_id"
WATSONX_URL="your_watsonx_url"
```

### 4. Add your PDFs
Drop your PDF files into the `data/` folder.

### 5. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
Sikkim_chatbot/
├── data/                    # PDF documents (taxi fares, history books)
├── vector_store/            # FAISS vector store (auto-generated)
├── app.py                   # Streamlit app + RAG pipeline
├── data_folder_hash.txt     # Hash file for auto-detecting new PDFs
├── requirements.txt
└── README.md
```

---

## 💡 What I'd Improve Next

- 🎨 Build a much better UI — current Streamlit UI is basic
- 🗣️ Add voice input for tourists on the go
- 🌐 Deploy online so tourists can access it anywhere
- 🗺️ Add map integration for tourist locations

---

## 👤 Author

**BrozG** — Full Stack & AI/ML Developer from Sikkim 🏔️

[![GitHub](https://img.shields.io/badge/GitHub-BrozG-blue)](https://github.com/BrozG)

---

## 📄 License

MIT
