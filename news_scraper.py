import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
# List to store articles
articles = []
def scrape_bbc():
    url = "https://www.bbc.com/news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    # Check response status
    if response.status_code != 200:
        print(f"Failed to retrieve data from BBC. Status code: {response.status_code}")
        return

    print("Successfully retrieved the BBC News page.")
    soup = BeautifulSoup(response.text, 'html.parser')
    # Use updated selectors based on the current HTML structure
    for item in soup.find_all('div', class_="sc-b38350e4-1 dlepEy"):
        try:
            # Ensure that the selectors are correct
            title_element = item.find('h2')
            summary_element = item.find('p')
            link_element = item.find('a')
            title_text = title_element.text.strip() if title_element else "No title available"
            summary_text = summary_element.text.strip() if summary_element else "No summary available"
            link = link_element.get('href') if link_element else "No link available"
            if not link.startswith("http"):
                link = "https://www.bbc.com" + link
            publication_date = item.find('span').get_text()
            source = "BBC"
            # Append the article data to the list
            articles.append({
                "title": title_text,
                "summary": summary_text,
                "date": publication_date,
                "source": source,
                "url": link
            })

        except Exception as e:
            print(f"Error while scraping: {e}")
            continue
def scrape_cnn():
    url = "https://timesofindia.indiatimes.com/toi-plus"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    # Check response status
    if response.status_code != 200:
        print(f"Failed to retrieve data from BBC. Status code: {response.status_code}")
        return

    print("Successfully retrieved the TOI News page.")
    soup1 = BeautifulSoup(response.text, 'html.parser')
    # Use updated selectors based on the current HTML structure
    for item in soup1.find_all('div', class_="Er0jX"):
        try:
            # Ensure that the selectors are correct
            title_element = item.find('h3')
            summary_element = item.find('p')
            link_element = item.find('a')
            title_text = title_element.text.strip() if title_element else "" 
            summary_text = summary_element.text.strip() if summary_element else ""
            link = link_element.get('href') if link_element else ""
            if not link.startswith("http"):
                link = "https://timesofindia.indiatimes.com/toi-plus" + link
            publication_date = item.find('span')
            publication_date = publication_date.get_text() if publication_date else ""
            source = "TOI"
            if (publication_date==''):
                continue
            else:
                articles.append({
                    "title": title_text,
                    "summary": summary_text,
                    "date": publication_date,
                    "source": source,
                    "url": link
                })

        except Exception as e:
            print(f"Error while scraping: {e}")
            continue
scrape_bbc()
scrape_cnn()
df = pd.DataFrame(articles)
df.to_csv("news_articles.csv", index=False)
print("Data saved to news_articles.csv")