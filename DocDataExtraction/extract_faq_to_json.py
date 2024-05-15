#!/usr/bin/env python
# coding: utf-8

# Script Overview

# This script reads the FAQ documents of DataTalksClub's courses, which are open and publicly available,
# and converts the documents to JSON format.

import io
import requests
import docx
import json

def clean_line(line):
    """Strip whitespace and BOM (Byte Order Mark) characters from the line."""
    line = line.strip()
    line = line.strip('\uFEFF')
    return line

def read_faq(file_id):
    """Read FAQ document from Google Docs and parse the questions and answers.

    Args:
        file_id (str): The Google Docs file ID.

    Returns:
        list: A list of dictionaries containing 'section', 'question', and 'text' keys.
    """
    url = f'https://docs.google.com/document/d/{file_id}/export?format=docx'
    
    # Download the document
    response = requests.get(url)
    response.raise_for_status()
    
    # Load the document content
    with io.BytesIO(response.content) as f_in:
        doc = docx.Document(f_in)

    questions = []

    question_heading_style = 'heading 2'
    section_heading_style = 'heading 1'
    
    section_title = ''
    question_title = ''
    answer_text_so_far = ''
    
    # Iterate through each paragraph in the document
    for p in doc.paragraphs:
        style = p.style.name.lower()  # Get the style of the paragraph
        p_text = clean_line(p.text)  # Clean the paragraph text
        
        if not p_text:
            continue  # Skip empty lines

        # Detect section headings
        if style == section_heading_style:
            section_title = p_text
            continue

        # Detect question headings
        if style == question_heading_style:
            # Save the previous question and answer if they exist
            if answer_text_so_far.strip() and section_title and question_title:
                questions.append({
                    'text': answer_text_so_far.strip(),
                    'section': section_title,
                    'question': question_title,
                })
                answer_text_so_far = ''  # Reset for the next question

            question_title = p_text
            continue

        # Accumulate the answer text
        answer_text_so_far += '\n' + p_text

    # Add the last question and answer to the list
    if answer_text_so_far.strip() and section_title and question_title:
        questions.append({
            'text': answer_text_so_far.strip(),
            'section': section_title,
            'question': question_title,
        })

    return questions

# Dictionary mapping course names to their corresponding Google Docs file IDs
faq_documents = {
    'data-engineering-zoomcamp': '19bnYs80DwuUimHM65UV3sylsCn2j1vziPOwzBwQrebw',
    'machine-learning-zoomcamp': '1LpPanc33QJJ6BSsyxVg-pWNMplal84TdZtq10naIhD8',
    'mlops-zoomcamp': '12TlBfhIiKtyBv8RnsoJR6F72bkPDGEvPOItJIxaEzE0',
}

documents = []

# Iterate over each course and its corresponding Google Docs file ID in the faq_documents dictionary
for course, file_id in faq_documents.items():
    print(course)  # Print the course name for debugging/monitoring purposes
    course_documents = read_faq(file_id)  # Read and parse the FAQ document for the course
    documents.append({'course': course, 'documents': course_documents})  # Append the parsed documents to the list

# Write the list of documents to a JSON file
with open('documents.json', 'wt') as f_out:
    json.dump(documents, f_out, indent=2)

get_ipython().system('head documents.json')
