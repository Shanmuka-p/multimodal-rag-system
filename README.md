# Multimodal RAG System

This project is a sophisticated Retrieval-Augmented Generation (RAG) system designed to answer questions over a collection of multimodal documents. It can understand and process information from text, images, and tables within PDFs and other document formats.

The system leverages state-of-the-art embedding models to create a searchable vector index of document contents and uses a powerful Vision-Language Model (VLM) like Gemini to generate accurate, context-aware answers.

## Architecture

For a detailed explanation of the system design, data flow, technology choices, and an architecture diagram, please see the [ARCHITECTURE.md](ARCHITECTURE.md) file.

*(Note: The `ARCHITECTURE.md` file is currently a placeholder. Please fill it with the relevant details of your system design.)*

## Features

*   **Multimodal Processing**: Extracts and understands text and images from PDF documents.
*   **Vector Embeddings**: Utilizes the `clip-ViT-B-32` model to generate embeddings for both text and images.
*   **Vector Store**: Uses ChromaDB for efficient storage and retrieval of vector embeddings.
*   **Generative Answering**: Employs Google's Gemini 1.5 Flash model to generate answers based on retrieved context.
*   **FastAPI Backend**: Exposes a clean and simple REST API for querying the system.
*   **Modular Design**: The codebase is organized into logical modules for ingestion, retrieval, and generation.

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

*   Python 3.8+
*   An API Key for Google Gemini. Get one here: [Google AI Studio](https://aistudio.google.com/app/apikey)
*   **Tesseract OCR Engine**: The `unstructured` library may require Tesseract for OCR capabilities. Please install it on your system:
    *   [Tesseract Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html)

### Setup Instructions

1.  **Clone the Repository**

    ```bash
    git clone <your-repository-url>
    cd multimodal-rag-system
    ```

2.  **Create a Virtual Environment**

    It's highly recommended to use a virtual environment to manage dependencies.

    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**

    Install all the required Python packages using the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables**

    The application requires a `GEMINI_API_KEY` to function. Create a `.env` file in the root of the project.

    ```bash
    # Create the .env file (e.g., using PowerShell on Windows)
    New-Item .env

    # Or on macOS/Linux
    touch .env
    ```

    Now, open the `.env` file and add your API key:

    ```
    GEMINI_API_KEY="your_gemini_api_key_here"
    ```

## How to Use

### 1. Ingest Documents

Before you can ask questions, you need to process your documents and load them into the vector database.

1.  Place all your documents (PDFs, PNG, JPG files) into the `sample_documents/` directory.
2.  Run the ingestion script:

    ```bash
    python src/ingestion/ingest.py
    ```

    This script will process each document, extract text and images, generate embeddings, and store them in the ChromaDB vector store (which will be created in a `chroma_db/` directory).

### 2. Run the API Server

Once ingestion is complete, start the FastAPI server.

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

The API server will be available at `http://localhost:8000`. You can access the interactive Swagger UI documentation at `http://localhost:8000/docs`.

### 3. Query the System

You can now send questions to the RAG system via the `/query` endpoint.

Here is an example using `curl`:

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "What were the total revenues in the last quarter?",
           "top_k": 5
         }'
```

The response will contain the generated answer and a list of the sources (text snippets or images) used to create that answer.

## Evaluation

The `evaluation.ipynb` Jupyter Notebook provides a framework for quantitatively assessing the performance of the RAG system.

To use it:
1.  Ensure you have Jupyter Notebook installed (`pip install jupyter`).
2.  Make sure the API server is running.
3.  Launch the notebook:

    ```bash
    jupyter notebook evaluation.ipynb
    ```

4.  Follow the instructions within the notebook to run sample queries and evaluate the retrieval and generation quality.

## Automated Testing

This project uses `pytest` for automated testing.

To run the test suite, execute the following command from the root directory:

```bash
pytest
```

This command will discover and run all the tests defined in the `tests/` directory.

## Submission Files

This repository includes several files required for project submission and automated evaluation:

*   **[ARCHITECTURE.md](ARCHITECTURE.md)**: Contains a detailed description of the system's architecture.
*   **[evaluation.ipynb](evaluation.ipynb)**: A Jupyter Notebook for evaluating the system's performance.
*   **[submission.yml](submission.yml)**: Defines the `setup` and `test` commands for automated evaluation.
    *(Note: This file is currently a placeholder. Please define the commands as shown below.)*

### `submission.yml` Configuration

Please ensure your `submission.yml` file contains the following content:

```yaml
setup: "pip install -r requirements.txt"
test: "pytest"
```
