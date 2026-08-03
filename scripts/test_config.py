from app.database.config import NEWS_API_KEY

if NEWS_API_KEY:
    print(f"✅ API key loaded ({len(NEWS_API_KEY)} characters)")
else:
    print("❌ API key not found")