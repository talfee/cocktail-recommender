from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
import requests
import faiss
import numpy as np
from PIL import Image
from flask_cors import CORS
from transformers import pipeline

# max number of cocktails to load
l = 1500

def load_cocktails(limit=l):
    resp = requests.get(
        "https://www.thecocktaildb.com/api/json/v1/1/filter.php",
        params={"c": "Cocktail"}
    )
    ids = [d["idDrink"] for d in resp.json().get("drinks", [])][:limit]

    data = []
    for drink_id in ids:
        lookup = requests.get(
            "https://www.thecocktaildb.com/api/json/v1/1/lookup.php",
            params={"i": drink_id}
        ).json().get("drinks", [None])[0]
        if not lookup:
            continue
        data.append({
            "name":        lookup.get("strDrink", ""),
            "description": lookup.get("strInstructions", "") or "",
            "image":       lookup.get("strDrinkThumb", "")
        })
    return data

# load and index
data         = load_cocktails(limit=l)
names        = [d["name"]        for d in data]
descriptions = [d["description"] for d in data]
images       = [d["image"]       for d in data]

# sentence‐BERT + FAISS
model = SentenceTransformer("clip-ViT-B-32")
embs  = model.encode(descriptions, normalize_embeddings=True).astype("float32")
dim   = embs.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(embs)

# flask app
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="templates/static"
)
CORS(app)

# switch to FLAN-T5 for instruction-tuned generation
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device=-1        # set to 0 if you have a GPU
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    # 1) embed the query (text or image)
    if request.content_type.startswith("application/json"):
        payload = request.get_json(force=True)
        q_emb = model.encode(
            [payload.get("query", "")], 
            normalize_embeddings=True
        ).astype("float32")
    else:
        #user query used for instrution prmpt
        user_q = request.form.get("query", "")
        file = request.files.get("image")
        img  = Image.open(file.stream).convert("RGB")
        q_emb = model.encode([img], normalize_embeddings=True).astype("float32")

    # 2) retrieve top-3 closest
    D, I = index.search(q_emb, k=3)
    results = [
        {
            "name":        names[idx],
            "description": descriptions[idx],
            "image":       images[idx],
            "similarity":  float(score) * 100
        }
        for score, idx in zip(D[0], I[0])
    ]

    # 3) build an instruction-driven prompt
    instruction = (
        f"You are a witty bartender AI."
        "Below are three other cocktails—explain, in two sentences, why they’re similar to (think shared ingredients or style) and add a playful flair:\n\n"
    )
    context = "\n".join(
        f"{i+1}. {r['name']}: {r['description']}"
        for i, r in enumerate(results)
    )
    prompt = instruction + context

    # 4) generate with sampling for creativity
    gen = generator(
        prompt,
        max_length=80,
        min_length=30,
        do_sample=True,
        temperature=1.5,
        top_k=100,
        top_p=0.95
    )
    recommendation = gen[0]["generated_text"].strip()

    # 5) return both
    return jsonify({
        "results":        results,
        "recommendation": recommendation
    })

if __name__ == "__main__":
    app.run(debug=True)
