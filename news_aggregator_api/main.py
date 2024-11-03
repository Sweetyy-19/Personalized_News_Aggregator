from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from datetime import datetime

app = FastAPI()

# Load the CSV data into a Pandas DataFrame
df = pd.read_csv("categorized_news_articles.csv")

# Function to handle NaN values and serialize to JSON
def serialize_df(df):
    df = df.fillna(0)  # Replace NaN with 0
    return df.to_dict(orient='records')

# Global variable to store serialized data
serialized_data = serialize_df(df)

@app.get("/")
async def root():
    return {"message": "News article"}

@app.get("/news")
async def get_news():
    return {"data": serialized_data}

@app.get("/articles")
async def get_articles(date: str = None,category: str = None):
    filtered_data = serialized_data.copy()
    if date:
        filtered_data = [article for article in filtered_data if date.lower() in f"{article['date']}".lower()]
    if category:
        filtered_data = [article for article in filtered_data if article['category'] == category]
    return {"data": filtered_data}

@app.get("/articles/{article_id}")
async def get_article(article_id: int):
    for article in serialized_data:
        if article['id'] == article_id:
            return JSONResponse(content=article)
    return JSONResponse(content={"message": "Article not found"}, status_code=404)

@app.get("/search")
async def search_news(keywords: str):
    filtered_data = [article for article in serialized_data if keywords.lower() in f"{article['title']}".lower()]
    if not filtered_data:
        return JSONResponse(content={"message": "No articles found for the given keywords"}, status_code=404)

    return {"data": filtered_data}

@app.get("/category")
async def search_news(category: str):
    filtered_data = [article for article in serialized_data if article['category'] == category]
    if not filtered_data:
        return JSONResponse(content={"message": "No articles found for that category"}, status_code=404)
    return {"data": filtered_data}

# Run the API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)