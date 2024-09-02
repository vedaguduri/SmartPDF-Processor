# SmartPDF-Processor
This repository contains a pipeline for extracting text from PDFs, generating summaries, creating flashcards, and forming search queries for images using OCR and OpenAI's GPT-3.5-turbo. It automates text data processing and includes utilities for fetching relevant images

README:
1. Overview
This project is a pipeline for processing PDFs and extracting key information such as text summaries, flashcards, and image search queries. It leverages OCR (Optical Character Recognition) with Tesseract, text processing with OpenAI's GPT-3.5 model, and web scraping using BeautifulSoup to fetch relevant images.

2. Setup and Installation
Prerequisites
Before running the pipeline, ensure you have the following installed:

Python 3.8+: You can download Python from python.org.
Tesseract OCR: Download and install Tesseract OCR from here.
Poppler: Install Poppler binaries for PDF to image conversion. You can download Poppler for Windows from here. Add the bin directory to your system's PATH.
pip: Python package installer.
Dependencies
Run the following command to install the required Python packages:

bash
Copy code
pip install pdf2image opencv-python numpy pytesseract openai requests beautifulsoup4
API Keys
OpenAI API Key: You need an API key from OpenAI to use the GPT-3.5 model. Obtain it by creating an account at OpenAI.
Set the API key in your script:
python
Copy code
openai.api_key = "your_openai_api_key"
Environment Setup
Clone the repository or download the source code.
Ensure the Poppler and Tesseract paths are correctly set in the script.
3. Running the Pipeline
To run the pipeline, follow these steps:

Prepare the Input PDF:

Place the PDF file in the desired location. Update the pdf_path in the script to point to your PDF file.
Run the Script:

Open a terminal or command prompt.
Navigate to the directory where the script is located.
Run the script using:
bash
Copy code
python your_script_name.py
Output:

The output files (output_summaries.json, output_flashcards.json, output_queries.json) will be saved to the specified paths.
4. Design Decisions
Modular Functions: Each function is designed to handle a specific task to improve readability and maintainability.
Error Handling: Basic error handling is implemented for image fetching and API calls to manage unexpected issues.
Efficient OCR: Preprocessing of images before OCR enhances text extraction accuracy.
Prompt Engineering: Specific prompts are designed for each task (summarization, flashcard generation, and search query creation) to ensure high-quality results.
5. Prompt Engineering Strategy
Summary Generation
Prompt Used:
plaintext
Copy code
Understand the text first and if the words are missing guess the relevant word and summarize the text:

{page_text[:1000]}
Rationale: This prompt encourages the model to infer missing words and produce a cohesive summary, addressing cases where OCR might miss parts of the text.
Flashcard Generation
Prompt Used:
plaintext
Copy code
Generate three flashcards (questions and answers) based on the text below. Each flashcard should be on a separate line, with the question on the first line and the answer on the second line:

{page_text[:1000]}
Rationale: This prompt instructs the model to generate concise questions and answers that highlight key points, facilitating learning and revision.
Search Query Generation
Prompt Used:
plaintext
Copy code
Based on the following text, create a concise and specific search query to find relevant images. Focus on key concepts, objects, or themes mentioned in the text, and include important keywords that would lead to relevant image results. Avoid overly generic terms:

{page_text[:1000]}
Rationale: This prompt aims to extract key concepts and relevant keywords from the text, generating targeted search queries for finding appropriate images.
6. Dependencies and Configuration
Ensure all necessary dependencies are installed and properly configured. Update paths for Poppler and Tesseract if required. The script is tested on Python 3.8+ and should be compatible with later versions.

7. Additional Notes
Security: Do not expose your OpenAI API key publicly. Store it securely, and consider using environment variables for better security.
Performance: The script is optimized for smaller PDFs. For larger files, consider breaking them into smaller chunks or pages.
8. Contributing
Feel free to fork the repository and submit pull requests for improvements or bug fixes. Contributions are always welcome!
