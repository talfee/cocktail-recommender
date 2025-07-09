# roundtwo

## demo
- python app.py
- go to https://cocktail-recommender.netlify.app/ 

## overview of app:
### walk through
1. app.py fetches drinks dataset from thecocktaildb (currently 1000 drinks)
2. transforms dataset using CLIP

### deliverbles
1. Data Preparation: fetched a dataset from TheCocktailDB API, each entry containing name, description, and image
2. Embedding Generation: used a CLIP‐based SentenceTransformer (clip-ViT-B-32) to encode cocktail descriptions into 512-dimension vectors.
3. Image Embeddings: the model encodes uploaded images (via PIL) into the same embedding space as text for image similarity search
4. Vector Database Setup: embeddings are stored in a FAISS IndexFlatIP in memory
5. Similarity Search & RAG: for similarity search, app.py detect whether the user sent text or an image, does query embedding, searches, and return the top 3 matches (name, image, description, similarity score). I used a local BART model from HuggingFace (distilbart-cnn-12-6) to generate a summary of the result. I want to transfer to Flan T5 for more generation capabilities
   
## things to do after mvp
### urgent/important
1. backend deployment
### non urgent/important
1. add testing suite
### features
1.  input cocktails

## setup commands
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask run ?

## learnings
1. how to deploy backend on render
fixing netlify "page not found" error: 
- this was caused by 
1. netlify not locating index.html since it was in templates
2. script.js defines BACKEND but all fetch calls use the relative path instead of \${BACKEND}/recommend, so the netlify deployment try to hit the netlify domain and not the flask server. since netlify has no configured /recommend endpoint, any request to that 404s
3. need to add a netlify.toml? --> this worked!

## credits
apis:
1. https://www.thecocktaildb.com/api.php

usage of AI
1. refactoring and bug fixes in multiple files (especially script.js)
2. majority of style.css, index.html for frontend