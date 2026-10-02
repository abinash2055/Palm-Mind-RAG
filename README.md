# Palm Mind AI — Conversational RAG Backend
---

## Overview
---

Backend implementation for the Palm Mind AI technical assignment.

The application provides:

1. Document ingestion
2. PDF/TXT text extraction
3. Two selectable chunking strategies
4. OpenAI embeddings
5. Qdrant vector storage
6. PostgreSQL metadata storage
7. Custom conversational RAG
8. Redis conversation memory
9. Multi-turn conversations
10. LLM-assisted interview booking

## Tech Stack
---

- FastAPI
- PostgreSQL
- Redis
- Qdrant
- OpenAI
- SQLAlchemy
- Alembic
- PyMuPDF
- pytest
- Docker


## Folder Structure
---

        📦app
        ┣ 📂 api
        ┃ ┣ 📂 routes
        ┃ ┣ 📜 __init__.py
        ┃ ┗ 📜 dependencies.py
        ┣ 📂 core
        ┃ ┣ 📜 __init__.py
        ┃ ┗ 📜 config.py
        ┣ 📂 db
        ┃ ┣ 📜 __init__.py
        ┃ ┣ 📜 database.py
        ┃ ┗ 📜 models.py
        ┣ 📂 sample_data
        ┃ ┣ 📜 doc1.txt
        ┃ ┣ 📜 doc2.txt
        ┃ ┣ 📜 doc3.txt
        ┃ ┗ 📜 sample.txt
        ┣ 📂 schema
        ┃ ┣ 📜 __init__.py
        ┃ ┣ 📜 booking.py
        ┃ ┣ 📜 chat.py
        ┃ ┗ 📜 document.py
        ┣ 📂 services
        ┃ ┣ 📜 __init__.py
        ┃ ┣ 📜 booking.py
        ┃ ┣ 📜 chunker.py
        ┃ ┣ 📜 embeddings.py
        ┃ ┣ 📜 ingestion.py
        ┃ ┣ 📜 llm.py
        ┃ ┣ 📜 memory.py
        ┃ ┣ 📜 parser.py
        ┃ ┣ 📜 rag.py
        ┃ ┗ 📜 vector_store.py
        ┣ 📂 tests
        ┃ ┣ 📜 __init__.py
        ┃ ┣ 📜 test_chunker.py
        ┃ ┣ 📜 test_documents.py
        ┃ ┗ 📜 test_parser.py
        ┣ 📜 __init__.py
        ┗ 📜 main.py


## Architecture 
---


                         CLIENT
                           │
                           ▼
                    ┌─────────────┐
                    │   FastAPI   │
                    └──────┬──────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
       Document API                  Chat API
             │                           │
             ▼                           ▼
       PDF/TXT Parser              Redis Memory
             │                           │
             ▼                           │
          Chunking                       │
       ┌─────┴─────┐                     │
       ▼           ▼                     │
    Fixed       Recursive                │
       │           │                     │
       └─────┬─────┘                     │
             ▼                           │
         Embeddings                      │
             │                           │
             ▼                           ▼
          Qdrant   ◄──────────────    Retrieval
             │                           │
             │                           ▼
             │                     RAG Context
             │                           │
             │                           ▼
             └──────────────────────► OpenAI
                                         │
                          ┌──────────────┴──────────────┐
                          ▼                             ▼
                       Answer                       Booking
                                                        │
                                                        ▼
                                                   PostgreSQL


## Setup
---

1. Install the programs\
    - Python 3.12+
    - Docker Desktop
    - PosgresSQL Application
    - Git
    - OpenAI API Key

2. Install All Dependencies
    - FastAPI application
    - PostgresSQL
    - Redis
    - Qdrant


## Environment Variables
---

1. APP_NAME
2. APP_ENV
3. DATABASE_URL for local and production
4. REDIS_URL for local and production
5. QDRANT_URL for local and production
6. QDRANT_COLLECTION
7. OPENAI_API_KEY
8. OPENAI_CHAT_MODEL
9. OPENAI_EMBEDDING_MODEL
10. TOP_K=5

### Running Locally

1. activate virtual Environment
2. Run the command
    - uvicorn app.main:app --reload


## API Endpoints
---

### Health

GET /health

### Document ingestion

POST /api/v1/documents/ingest

### Chat

POST /api/v1/chat

## Chunking Strategies
---

### Fixed
### Recursive


## RAG Pipeline
---

The application implements a custom Retrieval-Augmented Generation (RAG) pipeline without using RetrievalQAChain.
Document Ingestion

### The ingestion flow is:

        Upload PDF/TXT
            ↓
        Extract Text
            ↓
        Chunk Text
            ↓
        Generate Embeddings
            ↓
        Store Vectors in Qdrant
            ↓
        Store Metadata in PostgreSQL

The API supports two chunking strategies:

### Fixed chunking — splits text into chunks using a fixed size and overlap.
### Recursive chunking — recursively splits text using progressively smaller separators while attempting to preserve meaningful text boundaries.

### Retrieval and Generation
---

The conversational RAG flow is:

            User Question
                ↓
            Generate Query Embedding
                ↓
            Search Qdrant
                ↓
            Retrieve Relevant Chunks
                ↓
            Load Conversation History from Redis
                ↓
            Build Prompt
                ↓
                LLM
                ↓
            Answer + Sources

The retrieved document chunks are supplied as context to the language model. The model is instructed to answer using the available context rather than relying solely on its general knowledge.

The implementation performs retrieval and prompt construction explicitly rather than using RetrievalQAChain.

#### PostgreSQL:	Document and interview booking metadata
#### Qdrant:	    Document chunk embeddings and vector search
#### Redis:	        Conversational chat history
#### OpenAI:	    Embeddings and language-model generation


## Redis Memory
---

    Redis is used to maintain conversation history for multi-turn conversations.
    Each conversation is associated with a session_id.

### Example:
---

        {
        "session_id": "demo-session",
        "message": "What technologies does Abinash know?"
        }

### A follow-up message can reference the previous conversation:
---

        {
        "session_id": "demo-session",
        "message": "Which one does he use for API development?"
        }

The API retrieves the previous messages from Redis and includes the relevant conversation history when constructing the prompt.
This allows the application to understand follow-up questions without requiring the client to send the entire conversation history with every request.
Redis is used specifically for short-lived conversational state, while PostgreSQL and Qdrant are responsible for persistent application/document data.


## Interview Booking
---
Interview booking is handled through the conversational API.
The required booking information is:
        Name
        Email
        Date
        Time

The booking flow is designed to collect the required information through conversation.

### Example:
---
        User: I want to book an interview.
        Assistant: Sure. What is your name?

        User: Abinash Nath Pandey
        Assistant: What is your email?

        User: abinash@example.com
        Assistant: What date would you prefer?

        User: October 10, 2026
        Assistant: What time would you prefer?

        User: 10:00 AM

Once the required information has been collected, the booking data is validated and stored in PostgreSQL.
### The booking flow can be represented as:

            Conversation
                ↓
            Collect Booking Information
                ↓
            LLM-assisted Extraction
                ↓
            Validate Required Fields
                ↓
            Create Booking Record
                ↓
            Store in PostgreSQL

The booking information is persisted independently from Redis conversation history so that completed bookings are not dependent on the lifetime of a chat session.


## Testing
---

pytest

## Docker
---

docker compose up --build

## Design Decisions
---

### FastAPI

FastAPI was selected because the assignment requires REST APIs and it provides:

        Type-hinted request/response models
        Automatic OpenAPI documentation
        Async support
        Straightforward dependency injection
        Good integration with Python-based AI applications
        PostgreSQL

### PostgreSQL is used for structured application data such as:

        Document metadata
        File information
        Chunking strategy
        Booking information
        Timestamps

Relational storage is appropriate for data that requires predictable structure and validation.

### Qdrant
Qdrant is used as the vector database because the application requires semantic similarity search over document chunks.
Document embeddings are stored as vectors together with useful payload metadata such as document identifiers and chunk information.

### Redis
Redis is used for conversational memory because chat history requires fast read/write access and is naturally associated with a temporary conversation session.

### OpenAI Embeddings
Embeddings convert document chunks and user questions into numerical vector representations that can be compared for semantic similarity.
The same embedding model is used for both document chunks and incoming queries to keep them in the same vector space.

### Custom RAG Instead of RetrievalQAChain
The assignment explicitly requires a custom RAG implementation.
Therefore, retrieval, context construction, conversation-history handling, prompt construction, and LLM invocation are implemented as separate application components rather than relying on RetrievalQAChain.

### This also provides greater control over:

- Retrieved context
- Conversation memory
- Prompt structure
- Source information
- Booking-specific conversation handling
- Separation of Responsibilities

The application is divided into logical layers so that API routes do not contain the entire business logic.

### A simplified structure is:

            API Routes
                ↓
            Services
                ↓
            Repositories / Database Layer
                ↓
            External Services

This makes the code easier to test, maintain, and extend.

## Assumptions
---

### The following assumptions were made during implementation:

#### 1. PDF text extractio
Uploaded PDF files are assumed to contain machine-readable text. OCR is not included in this implementation.

#### 2. Supported file types
Only .pdf and .txt files are accepted by the document ingestion API.

#### 3. Chunking
The user can explicitly select between the supported fixed and recursive chunking strategies during ingestion.

#### 4. Vector storage
Qdrant is responsible for storing document embeddings and performing similarity search.

#### 5. Metadata storage
PostgreSQL stores document and booking metadata separately from the vector database.

#### 6. Conversation memory
Redis stores conversation history using a session identifier. Conversation history is treated as conversational state rather than permanent application data.

#### 7. Interview booking
A booking is created only after the required name, email, date, and time information has been collected and validated.

#### 8. Date and time
Interview date and time are stored according to the values supplied by the user. Time-zone conversion is outside the scope of this assignment unless explicitly configured.

#### 9. RAG context
Retrieved document chunks are treated as the primary context for answering document-related questions.

#### 10. No frontend
This implementation focuses only on the backend REST APIs because the assignment does not require a user interface.

#### 11. No OCR
Image-only/scanned PDFs are outside the current scope because OCR was not specified as a requirement.

#### 12. Authentication
Authentication is not included because it is not explicitly required by the assignment.

### 13. External services

OpenAI, Qdrant, Redis, and PostgreSQL are treated as external infrastructure/services and are configured through environment variables.

### 14. API keys and secrets

Sensitive credentials are provided through environment variables and are not committed to the repository.
