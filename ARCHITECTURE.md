# Multimodal RAG System Architecture

This document outlines the architecture of the Multimodal RAG (Retrieval-Augmented Generation) system. It describes the overall design, data flow, key components, and the technology choices made.

## 1. System Overview

The system is designed to answer user queries by retrieving relevant information from a collection of multimodal documents (containing text and images) and then generating a coherent answer based on the retrieved context.

The architecture is broken down into three main stages:
1.  **Ingestion**: Processing and indexing the source documents.
2.  **Retrieval**: Finding the most relevant document chunks (text or images) for a given query.
3.  **Generation**: Synthesizing an answer using a Vision-Language Model (VLM) based on the retrieved context.

![Architecture Diagram](https'://i.imgur.com/your-diagram-image.png') 
*(Please replace the above URL with an actual diagram illustrating the data flow described below.)*

---

## 2. Data Flow

The data flows through the system in two distinct phases:

### Ingestion Flow (Offline Processing)

1.  **Document Loading**: The process starts with PDF and image files located in the `sample_documents/` directory.
2.  **Parsing**: A `DocumentParser` processes each file. For PDFs, it uses the `PyMuPDF` library to extract raw text content and any embedded images on a page-by-page basis.
3.  **Chunking**: The extracted text from each page is passed to a `TextChunker`. This component splits long texts into smaller, semantically coherent chunks to ensure the embeddings are focused and meaningful.
4.  **Embedding**: Both text chunks and extracted images are then converted into vector embeddings. This is handled by a `MultimodalEmbedder` which uses the `sentence-transformers/clip-ViT-B-32` model. This model can create comparable vector representations for both text and images.
5.  **Indexing**: Each chunk (text or image) along with its embedding and metadata (e.g., original document ID, page number) is stored in a `ChromaDB` vector store. This creates a searchable index of the entire document collection.

### Query Flow (Real-time Processing)

1.  **API Request**: The user sends a query (e.g., "What were the key findings from the Q3 report?") to the FastAPI `/query` endpoint.
2.  **Query Embedding**: The user's query string is converted into a vector embedding using the same `clip-ViT-B-32` model that was used during ingestion.
3.  **Vector Search**: The `Retriever` component takes the query embedding and performs a similarity search against the ChromaDB index. It fetches the `top_k` most similar items (which can be either text chunks or image references).
4.  **Context Assembly**: The retrieved text chunks and images are collected to form a rich, multimodal context.
5.  **Answer Generation**: The original query and the retrieved context are passed to the `VLMGenerator`. This component uses the `gemini-1.5-flash` model. It constructs a prompt containing the user's question and the contextual information (both text and images).
6.  **API Response**: Gemini generates a final answer based on the provided context. This answer, along with metadata about the source documents it was derived from, is formatted and returned to the user as a JSON response.

---

## 3. Key Technology Choices

| Component             | Technology/Library           | Rationale                                                                                                                              |
| --------------------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Web Framework**     | `FastAPI`                    | Provides a high-performance, modern, and easy-to-use framework for building REST APIs, with automatic Swagger/OpenAPI documentation.      |
| **Document Parsing**  | `PyMuPDF`, `unstructured`    | `PyMuPDF` is highly efficient for extracting text and images from PDFs. `unstructured` offers robust, general-purpose document handling. |
| **Multimodal Model**  | `sentence-transformers/clip-ViT-B-32` | A powerful open-source model capable of creating semantically rich embeddings for both text and images in the same vector space.     |
| **Vector Database**   | `ChromaDB`                   | A lightweight and easy-to-use open-source vector store that can be run locally, making it ideal for development and prototyping.           |
| **Generative VLM**    | `Google Gemini 1.5 Flash`    | A fast, cost-effective, and highly capable multimodal model that can understand both text and images in its context window.                |
| **Environment Mgmt**  | `python-dotenv`              | Used to manage environment variables (like API keys) securely, separating configuration from code.                                     |
| **Testing**           | `pytest`                     | A standard, powerful, and easy-to-use testing framework for Python that simplifies writing and running tests.                            |

---
## 4. Code Structure

The source code in the `src/` directory is organized by functionality to ensure modularity and maintainability:

-   `src/api/`: Contains the FastAPI application (`main.py`) that serves the public-facing endpoints.
-   `src/ingestion/`: Houses all modules related to the offline data processing pipeline (`document_parser.py`, `chunker.py`, `ingest.py`).
-   `src/embeddings/`: Includes the `MultimodalEmbedder` for generating vector embeddings.
-   `src/vector_store/`: Contains the `ChromaManager` for interacting with the ChromaDB database.
-   `src/retrieval/`: Includes the `Retriever` class responsible for querying the vector store.
-   `src/generation/`: Contains the `VLMGenerator` class, which interfaces with the Gemini API to generate final answers.

This separation of concerns makes the system easier to debug, extend, and maintain.
