import pandas as pd
from elasticsearch import Elasticsearch, helpers
import csv

# Elasticsearch connection details
ELASTICSEARCH_HOST = "localhost"  # Replace with your Elasticsearch host
ELASTICSEARCH_PORT = 9200         # Replace with your Elasticsearch port

# CSV file path
CSV_FILE = "docs-metadata.csv"

# Index name
INDEX_NAME = "automation_docs"

def connect_elasticsearch():
    """Connects to Elasticsearch."""
    es = None
    try:
        es = Elasticsearch([{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT}])
        if es.ping():
            print("Connected to Elasticsearch")
        else:
            print("Could not connect to Elasticsearch!")
            return None
    except Exception as e:
        print(f"Error connecting to Elasticsearch: {e}")
        return None
    return es

def create_index(es, index_name):
    """Creates the Elasticsearch index with custom settings and mappings."""
    try:
        if not es.indices.exists(index=index_name):
            # Define index settings and mappings
            index_settings = {
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "tool": {"type": "keyword"},
                        "content": {"type": "text"},
                        "tags": {"type": "keyword"}
                    }
                }
            }
            es.indices.create(index=index_name, body=index_settings)
            print(f"Index '{index_name}' created successfully.")
        else:
            print(f"Index '{index_name}' already exists.")
    except Exception as e:
        print(f"Error creating index: {e}")

def prepare_actions(csv_file, index_name):
    """Prepares the documents for bulk indexing."""
    actions = []
    try:
        docs = pd.read_csv(csv_file)
        for _, row in docs.iterrows():
            # Data cleaning and transformation
            tags = row["tags"].split(",") if isinstance(row["tags"], str) else []  # Handle missing tags
            content = str(row["content"])  # Ensure content is a string

            action = {
                "_index": index_name,
                "_id": row["id"],
                "_source": {
                    "title": row["title"],
                    "tool": row["tool"],
                    "content": content,
                    "tags": tags
                }
            }
            actions.append(action)
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
        return None
    except csv.Error as e:
        print(f"Error reading CSV file: {e}")
        return None
    except Exception as e:
        print(f"Error preparing actions: {e}")
        return None
    return actions

def index_data(es, actions):
    """Indexes the data in bulk."""
    try:
        if actions:
            helpers.bulk(es, actions)
            print("
from transformers import pipeline  

nlp = pipeline("question-answering")  

def process_query(user_query):
    """Processes a user query by searching for relevant documents in Elasticsearch.

    Identifies entities in the user query and uses them to search for
    documents in the 'automation_docs' index that have matching tags.

    Args:
        user_query: The user's search query.

    Returns:
        The search results from Elasticsearch.
    """
    # Identifica entidades (ex: "Google Apps Script")
    entities = extract_entities(user_query)
    # Busca documentos relevantes no Elasticsearch
    results = es.search(index="automation_docs", body={
        "query": {
            "match": {
                "tags": " ".join(entities)
            }
        }
    })
    return results  
