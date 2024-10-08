from pdf2image import convert_from_path
import cv2
import numpy as np
import pytesseract
import openai
import re
import requests
import json
from bs4 import BeautifulSoup

openai.api_key = "add your api key"

def preprocess_image(image):
    grayscale = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    noise_reduced = cv2.medianBlur(grayscale, 3)
    binarized = cv2.threshold(noise_reduced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return binarized

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path, poppler_path=r"C:\poppler-24.07.0\Library\bin")
    text = []
    for i, image in enumerate(images):
        preprocessed_image = preprocess_image(image)
        ocr_text = pytesseract.image_to_string(preprocessed_image)
        if ocr_text:
            text.append(ocr_text)
        else:
            text.append(f"No text extracted from page {i + 1}")
    return text

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^A-Za-z0-9.,;:?!()\'"\s]', '', text)
    return text.strip()

def generate_summary(page_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"understand the text first and if the words are missing guess the relevant word and summarize the text:\n\n{page_text[:1000]}"}
        ]
    )
    summary = response['choices'][0]['message']['content']
    return summary

def generate_flashcards(page_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate three flashcards (questions and answers) based on the text below. Each flashcard should be on a separate line, with the question on the first line and the answer on the second line:\n\n{page_text[:1000]}"}
        ]
    )
    flashcards = response['choices'][0]['message']['content']
    return flashcards

def generate_search_query(page_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in generating search queries for images."},
            {"role": "user", "content": f"Based on the following text, create a concise and specific search query to find relevant images. Focus on key concepts, objects, or themes mentioned in the text, and include important keywords that would lead to relevant image results. Avoid overly generic terms:\n\n{page_text[:1000]}"}
        ]
    )
    search_query = response['choices'][0]['message']['content']
    return search_query

def fetch_image_urls(query):
    query = query.replace(' ', '+')
    url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        image_elements = soup.find_all('img')
        image_urls = []
        for img in image_elements:
            if 'src' in img.attrs and img['src'].startswith('http'):
                image_urls.append(img['src'])
            if len(image_urls) >= 10:
                break
        return image_urls
    except requests.exceptions.RequestException as e:
        print(f"Error fetching images: {e}")
        return []

def process_and_store_results(pdf_path, output_summary_file, output_flashcards_file, output_queries_file):
    extracted_text = extract_text_from_pdf(pdf_path)
    print(f"Extracted text from PDF: {extracted_text}")

    summaries = {}
    flashcards_dict = {}
    queries_and_images = {}

    for i, page_text in enumerate(extracted_text):
        print(f"\nProcessing Page {i + 1}...")
        page_id = f"Page {i + 1}"
        summaries[page_id] = {}
        flashcards_dict[page_id] = {}
        queries_and_images[page_id] = {}

        if "No text extracted" in page_text:
            print(page_text)
            summaries[page_id]["summary"] = page_text
            flashcards_dict[page_id]["flashcards"] = "No flashcards generated"
            queries_and_images[page_id]["query"] = "No query generated"
            queries_and_images[page_id]["images"] = "No images found"
            continue

        clean_page_text = clean_text(page_text)
        print(f"Cleaned Page Text: {clean_page_text}")
        summary = generate_summary(clean_page_text)
        print(f"Generated Summary: {summary}")
        summaries[page_id]["summary"] = summary
        flashcards = generate_flashcards(clean_page_text)
        print(f"Generated Flashcards: {flashcards}")
        flashcards_dict[page_id]["flashcards"] = flashcards
        search_query = generate_search_query(clean_page_text)
        print(f"Generated Search Query: {search_query}")
        queries_and_images[page_id]["query"] = search_query
        image_urls = fetch_image_urls(search_query)
        print(f"Curated Image URLs: {image_urls}")
        queries_and_images[page_id]["images"] = image_urls

    with open(output_summary_file, 'w', encoding='utf-8') as file:
        json.dump(summaries, file, ensure_ascii=False, indent=4)
    with open(output_flashcards_file, 'w', encoding='utf-8') as file:
        json.dump(flashcards_dict, file, ensure_ascii=False, indent=4)
    with open(output_queries_file, 'w', encoding='utf-8') as file:
        json.dump(queries_and_images, file, ensure_ascii=False, indent=4)

pdf_path = r"add pdf path"
output_summary_file = r"add your desired output location"
output_flashcards_file = r"add your desired output location"
output_queries_file = r"add your desired output location"

process_and_store_results(pdf_path, output_summary_file, output_flashcards_file, output_queries_file)
