# RAG Flask App with FlagReranker

A Flask API for document reranking using FlagReranker for Retrieval-Augmented Generation (RAG) systems.

## Features

- **Document Reranking**: Uses BAAI/bge-reranker-base model for accurate relevance scoring
- **RESTful API**: Clean JSON responses with proper error handling
- **Python 3.10 Compatible**: Modern Python with full type hint support
- **Easy Testing**: Includes Swagger documentation and HTML test interface

## Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd weaviate-rags

# Create virtual environment with Python 3.10
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python coursera/rags-101/flask_app.py
```

The API will be available at:
- http://localhost:5001
- http://127.0.0.1:5001

### 3. Test the API

#### Option A: Use the HTML Test Interface
Open `test_api.html` in your browser for an interactive testing interface.

#### Option B: Use Swagger UI
1. Go to https://editor.swagger.io/
2. Copy the contents of `swagger.yaml` into the editor
3. Use the "Try it out" feature to test endpoints

#### Option C: Use curl

```bash
# Test health endpoint
curl http://localhost:5001/health

# Test rerank endpoint
curl -X POST http://localhost:5001/rerank \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the capital of France?",
    "documents": ["Paris", "London", "Berlin", "Madrid"]
  }'
```

## API Endpoints

### GET /
Returns API information and available endpoints.

**Response:**
```json
{
  "message": "RAG Flask App with FlagReranker",
  "endpoints": {
    "/rerank": "POST - Rerank documents based on query relevance",
    "/health": "GET - Health check"
  }
}
```

### GET /health
Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "python_version": "3.10"
}
```

### POST /rerank
Reranks documents based on their relevance to a query.

**Request Body:**
```json
{
  "query": "What is the capital of France?",
  "documents": ["Paris", "London", "Berlin", "Madrid"]
}
```

**Response:**
```json
{
  "query": "What is the capital of France?",
  "total_documents": 4,
  "results": [
    {
      "document": "Paris",
      "relevance_score": 10.31,
      "rank": 1
    },
    {
      "document": "Madrid",
      "relevance_score": 9.64,
      "rank": 2
    },
    {
      "document": "London",
      "relevance_score": 6.07,
      "rank": 3
    },
    {
      "document": "Berlin",
      "relevance_score": 5.89,
      "rank": 4
    }
  ]
}
```

## Swagger Documentation

The complete API documentation is available in `swagger.yaml`. You can:

1. **View in Swagger Editor**: Copy the contents of `swagger.yaml` to https://editor.swagger.io/
2. **Generate client SDKs**: Use the Swagger file to generate client libraries
3. **Import into Postman**: Import the Swagger file into Postman for testing

## Example Use Cases

### 1. Capital Cities
```json
{
  "query": "What is the capital of France?",
  "documents": ["Paris", "London", "Berlin", "Madrid", "Rome"]
}
```

### 2. Weather Locations
```json
{
  "query": "What is the warmest place in the world?",
  "documents": ["Saudi Arabia", "India", "Arizona", "Brazil", "Australia"]
}
```

### 3. Technical Documentation
```json
{
  "query": "How to implement machine learning models?",
  "documents": [
    "Introduction to machine learning algorithms",
    "Deep learning with neural networks",
    "Data preprocessing techniques",
    "Model evaluation and validation",
    "Deployment strategies for ML models"
  ]
}
```

## Dependencies

- **Flask 2.3.3**: Web framework
- **FlagEmbedding 1.2.5**: Reranking model
- **PyTorch**: Deep learning framework
- **Transformers**: Hugging Face transformers library
- **NumPy**: Numerical computing
- **Joblib**: Model persistence

## Error Handling

The API returns appropriate HTTP status codes:

- **200**: Success
- **400**: Bad Request (missing required parameters)
- **405**: Method Not Allowed (wrong HTTP method)
- **500**: Internal Server Error

## Development

### Project Structure
```
weaviate-rags/
├── coursera/rags-101/
│   ├── flask_app.py          # Main Flask application
│   └── data.joblib           # Sample data file
├── venv/                     # Virtual environment
├── requirements.txt          # Python dependencies
├── swagger.yaml             # API documentation
├── test_api.html            # HTML test interface
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
