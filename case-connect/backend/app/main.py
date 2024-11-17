import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from FlagEmbedding import BGEM3FlagModel
import logging
import json

# Configura il logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)
CORS(app)

try:
    # Initialize model
    logger.info("Initializing BGEM3FlagModel...")
    model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
    logger.info("Model initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing BGEM3FlagModel: {e}")
    raise e

# Load embeddings data
embeddings_data = {}
base_path = "./data/embeddings"

@app.before_first_request
def initialize():
    logger.info("Initializing embeddings data...")
    base_path = "./data/embeddings"
    if not os.path.exists(base_path):
        logger.error(f"The embeddings directory '{base_path}' does not exist.")
        return

    datasets = os.listdir(base_path)
    logger.info(f"Found datasets: {datasets}")

    for dataset in datasets:
        dataset_path = os.path.join(base_path, dataset)
        logger.info(f"Processing dataset at {dataset_path}")

        # Ignora file che non sono directory
        if not os.path.isdir(dataset_path):
            logger.warning(f"Skipping non-directory {dataset_path}")
            continue

        try:
            embeddings_file = os.path.join(dataset_path, "embeddings_final.npy")
            metadata_file = os.path.join(dataset_path, "metadata_final.json")

            if not os.path.exists(embeddings_file) or not os.path.exists(metadata_file):
                logger.warning(f"Missing data files in {dataset_path}")
                continue

            embeddings = np.load(embeddings_file)
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            embeddings_data[dataset] = {
                "embeddings": embeddings,
                "metadata": metadata
            }
            logger.info(f"Loaded {dataset} with {len(metadata)} documents. Embeddings shape: {embeddings.shape}")
        except Exception as e:
            logger.error(f"Error loading {dataset}: {str(e)}")



@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/query', methods=['POST'])
def query_embeddings():
    data = request.json
    query = data.get("query", "")
    top_k = data.get("top_k", 5)

    if not query:
        return jsonify({"error": "Query text is required"}), 400

    try:
        logger.info(f"Received query: {query}")
        query_embedding = model.encode([query])['dense_vecs']
        logger.info(f"Query embedding shape: {query_embedding.shape}")

        results = []

        for dataset, content in embeddings_data.items():
            data_embeddings = content["embeddings"]
            logger.info(f"Dataset '{dataset}' embeddings shape: {data_embeddings.shape}")
            similarities = np.dot(query_embedding, data_embeddings.T).flatten()
            top_indices = similarities.argsort()[-top_k:][::-1]

            for idx in top_indices:
                similarity = float(similarities[idx])
                logger.info(f"Similarity for index {idx}: {similarity}")
                results.append({
                    "dataset": dataset,
                    "similarity": float(similarities[idx]),
                    "metadata": content["metadata"][idx]
                })

        results = sorted(results, key=lambda x: x["similarity"], reverse=True)[:top_k]
        return jsonify({
            "query": query,
            "results": results
        })

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)