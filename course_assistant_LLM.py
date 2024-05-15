#!/usr/bin/env python
# coding: utf-8

import json
from elasticsearch import Elasticsearch
from openai import OpenAI
from tqdm.auto import tqdm

def load_documents(file_path):
    """
    Load documents from a JSON file.
    
    Parameters:
    file_path (str): Path to the JSON file containing documents.
    
    Returns:
    list: List of dictionaries containing document information.
    """
    with open(file_path, 'rt') as file:
        documents_data = json.load(file)
    
    documents = []
    for course_info in documents_data:
        course_name = course_info['course']
        for doc in course_info['documents']:
            doc['course'] = course_name
            documents.append(doc)
    
    return documents

def create_index(es, index_name):
    """
    Create an Elasticsearch index.
    
    Parameters:
    es: Elasticsearch client.
    index_name (str): Name of the index to be created.
    
    Returns:
    dict: Response from Elasticsearch.
    """
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "section": {"type": "text"},
                "question": {"type": "text"},
                "course": {"type": "keyword"} 
            }
        }
    }
    
    return es.indices.create(index=index_name, body=index_settings)

def index_documents(es, index_name, documents):
    """
    Index documents into Elasticsearch.
    
    Parameters:
    es: Elasticsearch client.
    index_name (str): Name of the index where documents will be indexed.
    documents (list): List of dictionaries containing document information.
    
    Returns:
    None
    """
    for doc in tqdm(documents):
        es.index(index=index_name, body=doc)

def retrieve_documents(es, query, index_name="course-questions", max_results=5):
    """
    Retrieve documents from Elasticsearch based on a query.
    
    Parameters:
    es: Elasticsearch client.
    query (str): Query string.
    index_name (str): Name of the index to search in.
    max_results (int): Maximum number of results to retrieve.
    
    Returns:
    list: List of dictionaries containing retrieved documents.
    """
    search_query = {
        "size": max_results,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                },
                "filter": {
                    "term": {
                        "course": "data-engineering-zoomcamp"
                    }
                }
            }
        }
    }
    
    response = es.search(index=index_name, body=search_query)
    documents = [hit['_source'] for hit in response['hits']['hits']]
    return documents

def build_context(documents):
    """
    Build a context string from a list of documents.
    
    Parameters:
    documents (list): List of dictionaries containing document information.
    
    Returns:
    str: Context string.
    """
    context = ""
    for doc in documents:
        doc_str = f"Section: {doc['section']}\nQuestion: {doc['question']}\nAnswer: {doc['text']}\n\n"
        context += doc_str
    
    return context.strip()

def build_prompt(user_question, context):
    """
    Build a prompt for OpenAI GPT-3 chat completion.
    
    Parameters:
    user_question (str): User's question.
    context (str): Context string.
    
    Returns:
    str: Prompt string.
    """
    return f"""
You're a course teaching assistant.
Answer the user QUESTION based on CONTEXT - the documents retrieved from our FAQ database.
Don't use other information outside of the provided CONTEXT.

QUESTION: {user_question}

CONTEXT:

{context}
""".strip()

def ask_openai(prompt, client, model="gpt-3.5-turbo"):
    """
    Generate a response using OpenAI's chat completion API.
    
    Parameters:
    prompt (str): Prompt string.
    client: OpenAI client.
    model (str): Model name.
    
    Returns:
    str: Generated answer.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def qa_bot(user_question, es, openai_client):
    """
    QA bot that retrieves relevant documents and generates an answer.
    
    Parameters:
    user_question (str): User's question.
    es: Elasticsearch client.
    openai_client: OpenAI client.
    
    Returns:
    str: Generated answer.
    """
    context_docs = retrieve_documents(es, user_question)
    context = build_context(context_docs)
    prompt = build_prompt(user_question, context)
    answer = ask_openai(prompt, openai_client)
    return answer

if __name__ == "__main__":
    # Load documents
    documents = load_documents('./DocDataExtraction/documents.json')
    
    # Elasticsearch setup
    es = Elasticsearch("http://localhost:9200")
    index_name = "course-questions"
    
    # Create index
    create_index(es, index_name)
    
    # Index documents
    index_documents(es, index_name, documents)
    
    # User's question
    user_question = "How to run a dbt-core project as an Airflow Task Group on Google Cloud Composer using a service account JSON key?"
    
    # QA bot
    openai_client = OpenAI()
    answer = qa_bot(user_question, es, openai_client)
    
    print(answer)