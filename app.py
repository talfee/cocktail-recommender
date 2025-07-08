from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json


with open("cocktail_data.json") as f:
    data = json.load(f)
descriptions = [d["description"] for d in data]
names = [d["name"] for d in data]

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(descriptions, normalize_embeddings=True)
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(np.array(embeddings).astype("float32"))

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    query = request.json.get("query", "")
    q_emb = model.encode([query], normalize_embeddings=True)
    D, I = index.search(np.array(q_emb).astype("float32"), k=3)
    results = []
    for score, idx in zip(D[0], I[0]):
        results.append({
            "name": names[idx],
            "description": descriptions[idx],
            "similarity": float(score) * 100
        })
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
