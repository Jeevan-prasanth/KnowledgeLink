# KnowledgeLink
Multimodel Rag


## Overview

The Multimodel Chatbot is a Retrieval-Augmented Generation (RAG) chatbot that allows users to interact with PDF documents, URL, Audio ,images and Video locally. The entire application, including the language models and vector database, runs locally on your machine. This chatbot leverages the following models and frameworks:
- **Chat Model:** Llama3
- **Image Model:** Llava
- **Embeddings:** mxbai-embed-large
- **Vector Database:** Qdrant

The application provides a Streamlit-based user interface where users can upload PDF documents,images,Url,Audio and Video link, ask questions about the uploaded content, and receive detailed responses. 

## Features

### Chat with PDF
Upload a PDF document and ask questions about its content. This feature allows for easy extraction of information and a better understanding of the document.

**Usage:**
1. Upload your PDF file.
2. Ask questions related to the content of the PDF.

### Image Description
Upload an image and receive a detailed description of it. This feature helps in understanding the contents and context of the image.

**Usage:**
1. Upload your image file.
2. Receive a detailed description of the image.

### Add URL
Provide a URL to retrieve and discuss content from the linked page. This is useful for exploring web content directly through the chat interface.

**Usage:**
1. Submit a URL.
2. Get a summary or detailed discussion of the content from the linked page.

### Audio Description
Upload an audio file and get a detailed description or transcription of it. This is helpful for extracting information from audio sources.

**Usage:**
1. Upload your audio file.
2. Receive a detailed description or transcription of the audio content.

### Video Description
Upload a video file and get a detailed description or transcription of its content. This is useful for understanding video content without needing to watch it.

**Usage:**
1. Upload your video file.
2. Receive a detailed description or transcription of the video content.


## Setup Instructions

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.8 or higher
- Poetry (a dependency management tool for Python)
- Ollama (a tool for managing and running large language models locally)

### Installation Steps

1. **Clone the repository**
   ```sh
   git clone https://github.com/Jeevan-prasanth/KnowledgeLink.git
   ```

2. **Navigate to the project directory**
   ```sh
   cd KnowledgeLink
   ```

3. **Set up a virtual environment**
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

4. **Install Poetry**
   ```sh
   pip install poetry
   ```

5. **Install project dependencies**
   ```sh
   poetry install
   ```

6. **Pull required models using Ollama**
   ```sh
   ollama pull mxbai-embed-large
   ollama pull llava
   ollama pull llama3
   ```

### Running the Application

To start the Streamlit user interface, run:
```sh
poetry run streamlit run app/main.py
```

This command will launch the Streamlit application in your default web browser. You will be greeted with an interface to upload your PDF documents and images.

## Project Structure

```
├── app
│   ├── main.py
├── pdf_img_chatbot
│   ├── chatbot.py
│   ├── documents_loader
│   │   ├── __pycache__
│   │   │   └── unstructured.cpython-312.pyc
│   │   └── unstructured.py
│   ├── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── olllama.py
│   │   └── __pycache__
│   │       ├── __init__.cpython-312.pyc
│   │       └── olllama.cpython-312.pyc
│   ├── prompts
│   │   ├── __pycache__
│   │   │   └── rag.cpython-312.pyc
│   │   └── rag.py
│   ├── __pycache__
│   │   ├── chatbot.cpython-312.pyc
│   │   └── __init__.cpython-312.pyc
│   └── vector_db
│       ├── __pycache__
│       │   └── qdrant.cpython-312.pyc
│       └── qdrant.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── tests
    └── __init__.py
```

## Additional Notes

- Ensure that your system has sufficient resources (CPU, RAM) to handle the large models being used.
- For optimal performance, it's recommended to run the application on a machine with a dedicated GPU.
- If you encounter any issues, please refer to the official documentation of the respective tools and frameworks being used.
