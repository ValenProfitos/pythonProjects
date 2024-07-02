import requests
import sys
import csv

def get_company_name(ticker):
    ticker_to_company = {
        "GOOG": "Google",
        "TSLA": "Tesla",
        # Añade más mapeos según sea necesario
    }
    return ticker_to_company.get(ticker, "")

def fetch_articles(company_name):
    url = f'https://www.reuters.com/pf/api/v3/content/fetch/articles-by-search-v2?query=%7B%22keyword%22%3A%22{company_name}%22%2C%22offset%22%3A0%2C%22orderby%22%3A%22display_date%3Adesc%22%2C%22size%22%3A20%2C%22website%22%3A%22reuters%22%7D&d=201&_website=reuters'
    headers = {
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'Referer': f'https://www.reuters.com/site-search/?query={company_name}&offset=0',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/126.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    results = []
    for article in data['result']['articles']:
        title = article['title']
        link = article['canonical_url']
        summary = article.get('description', "")
        results.append({
            "Title": title,
            "Link": f'https://www.reuters.com{link}',
            "Summary": summary
        })

    return results

def save_to_csv(articles, company_name):
    with open(f'{company_name}_articles.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Link", "Summary"])
        writer.writeheader()
        for article in articles:
            writer.writerow(article)
    print(f"Results downloaded in {company_name}_articles.csv")

def main(ticker):
    company_name = get_company_name(ticker)
    if not company_name:
        print("Company's name not found")
        return
    
    articles = fetch_articles(company_name)
    save_to_csv(articles, company_name)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: python scrape_reuters.py <TICKER>")
    else:
        ticker = sys.argv[1]
        main(ticker)