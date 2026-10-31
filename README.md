# Retrieval-Augmented Generation (RAG) System

A Python-based Retrieval-Augmented Generation (RAG) project that processes PDF documents, extracts text, divides documents into meaningful chunks, generates vector embeddings, and stores them in ChromaDB for semantic search and context retrieval.

## Overview

Retrieval-Augmented Generation (RAG) combines information retrieval with generative AI. Instead of relying only on the knowledge stored in a language model, RAG retrieves relevant information from external documents and uses it as context to generate more relevant, document-grounded answers.

This project implements the core RAG pipeline using Python, Sentence Transformers, and ChromaDB.

## Architecture

```text
        PDF Documents
              |
              v
       Document Ingestion
              |
              v
        Text Extraction
              |
              v
         Text Chunking
              |
              v
       Embedding Generation
              |
              v
          ChromaDB
        Vector Database
              |
       User Query
              |
              v
        Query Embedding
              |
              v
       Semantic Retrieval
              |
              v
      Relevant Context
              |
              v
       Answer Generation
              |
              v
         Final Answer
```

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Sentence Transformers | Text embedding generation |
| all-MiniLM-L6-v2 | Pre-trained embedding model |
| ChromaDB | Vector database |
| PyPDF | PDF text extraction |
| NumPy | Numerical operations |

## Project Structure

```text
Retrieval-Augmented-Generation/
│
├── data/                  # Input PDF documents
│
├── ingestion/
│   ├── ingest.py          # Document ingestion
│   ├── chunk.py           # Text chunking
│   ├── embedding.py       # Embedding generation
│   ├── verify_embeddings.py
│   ├── vector_db.py       # Vector database operations
│   └── pipeline.py        # Ingestion pipeline
│
├── retrieval/             # Document retrieval
│
├── generation/            # Answer generation
│
├── rag.py                 # Main RAG application
│
├── requirements.txt       # Python dependencies
│
└── README.md
```

## Key Features

- PDF document ingestion and text extraction.
- Document preprocessing and text chunking.
- Semantic embedding generation using Sentence Transformers.
- 384-dimensional vector embeddings using all-MiniLM-L6-v2.
- Persistent vector storage using ChromaDB.
- Metadata storage, including document name, page number, file type, and source path.
- Semantic similarity-based document retrieval.
- Retrieval pipeline designed to provide relevant context for answer generation.

## RAG Workflow

### 1. Document Ingestion
PDF documents are loaded from the data directory and their text content is extracted.

### 2. Text Chunking
Extracted text is divided into smaller chunks to improve retrieval accuracy and make document processing more efficient.

### 3. Embedding Generation
The Sentence Transformer model `all-MiniLM-L6-v2` converts text chunks into numerical vector representations.

### 4. Vector Database
The generated embeddings and associated metadata are stored in ChromaDB for efficient similarity search.

### 5. Retrieval
When a user submits a query, it is converted into an embedding and compared with stored document embeddings to retrieve relevant chunks.

### 6. Answer Generation
The retrieved context can be passed to a language model to generate a response grounded in the source documents.

## Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/sumanth1709/Retrieval-Augmented-Generation.git
```

**2. Navigate to the project directory**

```bash
cd Retrieval-Augmented-Generation
```

**3. Create a virtual environment**

```bash
python -m venv .venv
```

**4. Activate the virtual environment (Windows PowerShell)**

```powershell
.venv\Scripts\Activate.ps1
```

**5. Install dependencies**

```bash
pip install -r requirements.txt
```

## Running the Project

1. Place your PDF documents inside the `data/` directory.
2. Run the ingestion pipeline:

```bash
python ingestion/pipeline.py
```

3. Verify the generated embeddings and vector database.
4. Run the main RAG application:

```bash
python rag.py
```

*Note: The commands and required configuration may need adjustment depending on the current implementation of your scripts.*

## Embedding Model

**Model:** `sentence-transformers/all-MiniLM-L6-v2`

- Embedding dimension: 384
- Framework: Sentence Transformers
- Purpose: Semantic representation of text for similarity-based retrieval.

## Vector Database

**ChromaDB**

ChromaDB is used to store and retrieve document embeddings. It supports similarity-based searches and metadata filtering.

## Future Enhancements

- Integrate advanced language models for answer generation.
- Implement an Agentic RAG architecture.
- Add hybrid search using keyword and semantic retrieval.
- Improve retrieval accuracy using reranking.
- Develop a user-friendly web interface.
- Add source citations to generated answers.

## Author

**Sumanth Reddy**

GitHub: [@sumanth1709](https://github.com/sumanth1709)

## License

This project is intended for educational and research purposes.
