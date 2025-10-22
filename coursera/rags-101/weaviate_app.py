import os
import json
import logging
from pathlib import Path
import subprocess
from openai import OpenAI

logger = logging.getLogger(__name__)

def load_openai_config():
    """Load configuration from openai-config.json file in user's home directory"""
    config_path = Path.home() / "openai-config.json"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    api_key = config.get('api_key')
    model = config.get('model', 'text-embedding-3-small')
    logger.info(f"Loaded OpenAI configuration: model={model}")
    return api_key, model

def generate_embedding(prompt: str, **kwargs):
    """Generate embeddings using OpenAI's API"""
    # Load configuration from file
    api_key, model = load_openai_config()
    
    # Fallback to environment variable if not in config file
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")
    
    if api_key is None:
        raise ValueError("OpenAI API key is required. Set it in ~/openai-config.json or OPENAI_API_KEY environment variable")

    client = OpenAI(api_key=api_key)
    
    response = client.embeddings.create(
        input=prompt,
        model=model,
        **kwargs
    )
    
    return response.data[0].embedding

if __name__ == "__main__":
    embedding = generate_embedding("Capital of France is not here")
    logger.info(f"Generated embedding with {len(embedding)} dimensions")
    print(f"Embedding dimensions: {embedding}")
    subprocess.Popen