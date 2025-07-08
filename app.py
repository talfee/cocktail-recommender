from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
import requests
import faiss
import numpy as np
from PIL import Image
from flask_cors import CORS

# variables
l = 1500

def load_cocktails(limit=l):
    resp = requests.get(
        "https://www.thecocktaildb.com/api/json/v1/1/filter.php",
        params={"c": "Cocktail"}
    )
    ids = [d["idDrink"] for d in resp.json().get("drinks", [])][:limit]

    data = []
    for drink_id in ids:
        r2 = requests.get(
            "https://www.thecocktaildb.com/api/json/v1/1/lookup.php",
            params={"i": drink_id}
        ).json().get("drinks", [None])[0]
        if not r2:
            continue
        data.append({
            "name":        r2.get("strDrink", ""),
            "description": r2.get("strInstructions", "") or "",
            "image":       r2.get("strDrinkThumb", "")
        })
    return data

data = load_cocktails(limit=l)
names        = [d["name"]        for d in data]
descriptions = [d["description"] for d in data]
images       = [d["image"]       for d in data]

model     = SentenceTransformer("clip-ViT-B-32")
embs      = model.encode(descriptions, normalize_embeddings=True).astype("float32")

dim       = embs.shape[1]
index     = faiss.IndexFlatIP(dim)
index.add(embs)

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="templates/static"    # ← point here
)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    if request.content_type.startswith("application/json"):
        payload = request.get_json(force=True)
        q_emb   = model.encode([ payload.get("query","") ], normalize_embeddings=True).astype("float32")
    else:
        file    = request.files.get("image")
        img     = Image.open(file.stream).convert("RGB")
        q_emb   = model.encode([ img ], normalize_embeddings=True).astype("float32")

    D, I = index.search(q_emb, k=3)

    results = []
    for score, idx in zip(D[0], I[0]):
        results.append({
            "name":        names[idx],
            "description": descriptions[idx],
            "image":       images[idx],
            "similarity":  float(score) * 100
        })
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
