# roundtwo

## overview of app:
1. app.py fetches drinks dataset from thecocktaildb (currently 1000 drinks)
2. transforms dataset using CLIP
   
## things to do after mvp
### urgent/important
1. deployment
- frontend: fixing the issues
- backend: why memory? 
### non urgent/important
1. add testing suite
features
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
2. m

## credits
apis:
1. https://www.thecocktaildb.com/api.php

usage of AI
1. refactoring in multiple files
2. majority of style.css, index.html for frontend