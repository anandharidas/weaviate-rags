from flask import Flask, request, jsonify
import threading
import json
from FlagEmbedding import FlagReranker

reranker = FlagReranker('BAAI/bge-reranker-base')

scores = reranker.compute_score([
    ["What is the capital of France?", "Paris"],
    ["What is the capital of France?", "London"],
    ["What is the capital of France?", "Berlin"],
    ["What is the capital of France?", "Madrid"],
    ["What is the warmest place in the world?", "Saudi Arabia"],
    ["What is the warmest place in the world?", "London"],
    ["What is the warmest place in the world?", "India"],
    ["What is the warmest place in the world?", "Arizona"]
])

print(scores)

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "RAG Flask App with FlagReranker",
        "endpoints": {
            "/rerank": "POST - Rerank documents based on query relevance",
            "/health": "GET - Health check"
        }
    })

@app.route('/rerank', methods=['POST'])
def rerank_documents():
    try:
        data = request.get_json()
        query = data.get('query', '')
        documents = data.get('documents', [])
        
        if not query or not documents:
            return jsonify({"error": "Query and documents are required"}), 400
        
        # Create query-document pairs for reranking
        pairs = [[query, doc] for doc in documents]
        
        # Compute reranking scores
        scores = reranker.compute_score(pairs)
        
        # Combine documents with their scores and sort by score (descending)
        results = []
        for i, (doc, score) in enumerate(zip(documents, scores)):
            results.append({
                "document": doc,
                "relevance_score": float(score),
                "rank": i + 1
            })
        
        # Sort by relevance score (descending)
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Update ranks after sorting
        for i, result in enumerate(results):
            result['rank'] = i + 1
        
        return jsonify({
            "query": query,
            "total_documents": len(documents),
            "results": results
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "python_version": "3.10"})

if __name__ == '__main__':
    print("Starting Flask app with FlagReranker...")
    print("Visit http://localhost:5001 for the API")
    app.run(debug=True, host='0.0.0.0', port=5001)