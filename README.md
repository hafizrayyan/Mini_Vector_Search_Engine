# Mini Vector Search Engine

A semantic search application that lets you upload PDF documents and search through them using natural language — just like Google, but for your own files.

---

## What does it do?

You upload PDF files, and the app lets you search through them by meaning — not just keywords.

For example, if your PDF talks about "neural networks", searching for **"how does the brain inspire AI?"** will still find the right paragraph — because the app understands meaning, not just exact words.

---

## Built With

| Tool | Purpose |
|---|---|
| Streamlit | Web interface |
| PyPDF | Extract text from PDFs |
| Sentence Transformers | Convert text into vectors |
| Pinecone | Store and search vectors |

---

## How to Use
https://vector-search-engine-by-hafiz-rayyan.streamlit.app/

1. Open the app in your browser
2. Upload up to 5 PDF files
3. Wait for them to be processed
4. Type your question in the search box
5. Click **Search** — results appear instantly with the source file and match score

---

## Author

**Hafiz Rayyan**
