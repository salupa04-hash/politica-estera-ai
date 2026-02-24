import requests
import pandas as pd
import spacy
from transformers import pipeline
from newspaper import Article
import os

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

QUERY = "foreign policy OR sanctions OR diplomatic agreement"
URL = "https://newsapi.org/v2/everything"

params = {
    "q": QUERY,
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": 20,
    "apiKey": NEWSAPI_KEY
}

response = requests.get(URL, params=params).json()
articles = response.get("articles", [])

nlp = spacy.load("en_core_web_sm")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

EVENT_TYPES = [
    "sanction imposed",
    "diplomatic agreement",
    "military intervention",
    "policy announcement",
    "treaty withdrawal",
    "economic cooperation"
]

results = []

for art in articles:
    try:
        article = Article(art["url"])
        article.download()
        article.parse()
        text = article.text[:2000]

        classification = classifier(text, EVENT_TYPES)
        top_event = classification["labels"][0]
        score = classification["scores"][0]

        if score >= 0.6:
            results.append({
                "Titolo": art["title"],
                "Evento": top_event,
                "Confidenza": round(score, 3),
                "Link": art["url"]
            })

    except:
        continue

df = pd.DataFrame(results)
df.to_csv("politica_estera_AI_finale.csv", index=False, sep=";")
