from flask import Flask, request, jsonify
import threading
import json
import re
from collections import Counter

def simple_text_similarity(query, document):
    """Simple text similarity based on word overlap"""
    query_words = set(re.findall(r'\w+', query.lower()))
    doc_words = set(re.findall(r'\w+', document.lower()))
    
    if not query_words or not doc_words:
        return 0.0
    
    intersection = query_words.intersection(doc_words)
    union = query_words.union(doc_words)
    
    return len(intersection) / len(union) if union else 0.0

# Example queries and documents
queries = ["What is the capital of France?", "What is the warmest place in the world?"]
documents = ["Paris", "London", "Berlin", "Madrid", "Saudi Arabia", "India", "Arizona"]

# Compute similarity scores
print("Similarity scores:")
for i, query in enumerate(queries):
    print(f"\nQuery: {query}")
    for j, doc in enumerate(documents):
        score = simple_text_similarity(query, doc)
        print(f"  {doc}: {score:.3f}")

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "RAG Flask App with Text Similarity",
        "endpoints": {
            "/similarity": "POST - Calculate similarity between query and documents",
            "/health": "GET - Health check"
        }
    })

@app.route('/similarity', methods=['POST'])
def calculate_similarity():
    try:
        data = request.get_json()
        query = data.get('query', '')
        documents = data.get('documents', [])
        
        if not query or not documents:
            return jsonify({"error": "Query and documents are required"}), 400
        
        results = []
        for doc in documents:
            score = simple_text_similarity(query, doc)
            results.append({"document": doc, "similarity_score": score})
        
        # Sort by similarity score (descending)
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return jsonify({
            "query": query,
            "results": results
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    print("Starting Flask app...")
    print("Visit http://localhost:5000 for the API")
    app.run(debug=True, host='0.0.0.0', port=5000)