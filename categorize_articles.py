import pandas as pd

# Load the CSV file
data = pd.read_csv('news_articles.csv')

data['id'] = range(1, len(data) + 1)  # ID starts from 1; change to `range(len(data))` to start from 0

import spacy

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    # Use spaCy to process the text
    doc = nlp(text)
    # Remove stop words and punctuation, and return a list of clean words
    return ' '.join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

# Apply preprocessing to the 'Summary' column
data['summary'] = data['summary'].apply(preprocess)


def categorize_article(summary):
    # Define keywords for different categories
    categories = {
        'Politics': ['government', 'election', 'politics', 'political', 'party','president'],
        'Technology': ['technology', 'tech', 'AI', 'machine learning', 'software', 'hardware'],
        'Sports': ['sports', 'game', 'team', 'match', 'football', 'basketball','league'],
        'Health': ['health', 'disease', 'medicine', 'doctor', 'treatment'],
        'Business': ['business', 'economy', 'market', 'finance', 'investment']
    }
    
    # Check for keywords in the summary and assign a category
    for category, keywords in categories.items():
        if any(keyword in summary.lower() for keyword in keywords):
            return category
    
    return 'Other'  # Return 'Other' if no keywords match

# Apply categorization to the cleaned summaries
data['category'] = data['summary'].apply(categorize_article)

# Save the updated DataFrame to a new CSV file
data.to_csv('news_aggregator_api/categorized_news_articles.csv', index=False)

