import json
from recommender.pipeline import ProductRecommendationPipeline

with open("data/products_full.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

pipeline = ProductRecommendationPipeline()
pipeline.build_index(DATA)

def get_recommendation(query: str) -> str:
    response = pipeline.recommend(query)
    return response.content.strip()