Here's a more concise README suitable for your repository:

---

# SmartPDF-Processor

This repository contains a pipeline for extracting text from PDFs, generating summaries, creating flashcards, and forming search queries for images using OCR and OpenAI's GPT-3.5-turbo. It automates text data processing and includes utilities for fetching relevant images.

## Overview
A pipeline to process PDFs and extract information like summaries, flashcards, and image search queries using Tesseract OCR, OpenAI's GPT-3.5, and BeautifulSoup for web scraping.

## Setup and Installation

### Prerequisites
- **Python 3.8+**
- **Tesseract OCR**: Install from [here](https://github.com/tesseract-ocr/tesseract).
- **Poppler**: Download from [here](https://poppler.freedesktop.org/). Add the `bin` directory to your PATH.

### Install Dependencies
```bash
pip install pdf2image opencv-python numpy pytesseract openai requests beautifulsoup4
```

### API Keys
- Obtain an OpenAI API key from [OpenAI](https://openai.com/). Add to your script:
```python
openai.api_key = "your_openai_api_key"
```

### Environment Setup
1. Clone the repository or download the source code.
2. Ensure Poppler and Tesseract paths are correctly set.

## Running the Pipeline

1. **Prepare the Input PDF**: Update `pdf_path` in the script.
2. **Run the Script**:
   ```bash
   python your_script_name.py
   ```
3. **Output**: JSON files (summaries, flashcards, queries) will be saved to specified paths.

## Design Decisions
- **Modular Functions** for better readability and maintainability.
- **Error Handling** for robustness.
- **Efficient OCR** with pre-processing.
- **Prompt Engineering** to ensure high-quality results.

## Prompt Engineering Strategy

- **Summary Generation**: Instructs the model to infer missing words and summarize coherently.
- **Flashcard Generation**: Directs the model to create concise Q&A pairs for key points.
- **Search Query Generation**: Extracts keywords for targeted image search queries.

## Dependencies and Configuration
Ensure dependencies are installed and paths configured. Tested on Python 3.8+.

## Additional Notes
- **Security**: Protect your OpenAI API key.
- **Performance**: Optimize for smaller PDFs.

## Contributing
Fork the repository and submit pull requests for any improvements or bug fixes.

---

