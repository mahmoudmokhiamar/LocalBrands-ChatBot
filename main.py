import json
from recommender.pipeline import ProductRecommendationPipeline
import warnings
warnings.filterwarnings("ignore")

def load_data():
    with open("data/products_full.json", "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    print("📦 Loading product data...")
    data = load_data()

    print("🚀 Starting recommendation pipeline...")
    pipeline = ProductRecommendationPipeline()
    pipeline.build_index(data)

    query = input("\n💬 What are you looking for? ").strip()
    response = pipeline.recommend(query)

    print("\n🤖 AI Recommendation:\n")
    print(response.content.strip())