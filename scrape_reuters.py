import requests
import sys
import csv

def get_company_name(ticker):
    api_key= 'UIXBF42YPFKR9OFU'
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        company_name = data.get('Name', '')
        for suffix in [' Inc', ' Corporation', ' Limited', '.com', ' Corp', ' Ltd', ' Holdings', ' Group']:
            company_name = company_name.replace(suffix, '').replace(suffix + '.','').strip()
        
        if ticker == "GOOGL" or ticker == "GOOG":
            company_name = "Google"
            
        return company_name
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Error obtaining company's name: {err}")
    return None

def fetch_articles(company_name):
    print(f"Fetching articles for: {company_name}")
    url = f'https://www.reuters.com/pf/api/v3/content/fetch/articles-by-search-v2?query=%7B%22keyword%22%3A%22{company_name}%22%2C%22offset%22%3A0%2C%22orderby%22%3A%22display_date%3Adesc%22%2C%22size%22%3A20%2C%22website%22%3A%22reuters%22%7D&d=201&_website=reuters'
    headers = {
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'Referer': f'https://www.reuters.com/site-search/?query={company_name}&offset=0',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/126.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        articles = data.get('result',{}).get('articles',[])

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

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error ocurred: {http_err}")
    except Exception as err:
        print(f"Error obtaining articles: {err}")
    return []

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
    if articles:
        save_to_csv(articles, company_name)
    else:
        print(f"No articles found for {company_name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scrape_reuters.py <TICKER>")
    else:
        ticker = sys.argv[1]
        main(ticker)