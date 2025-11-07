import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path

def scrape_pg_essays(max_essays=40):
    
    base_url = "http://www.paulgraham.com/"
    essays_url = base_url + "articles.html"
    
    print(f"Fetching essay list from {essays_url}...")
    response = requests.get(essays_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    essay_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith('.html') and href != 'articles.html':
            essay_links.append({
                'title': link.text.strip(),
                'url': base_url + href
            })
    
    essay_links = essay_links[:max_essays]
    
    essays_data = []
    for i, essay in enumerate(essay_links, 1):
        print(f"Scraping {i}/{len(essay_links)}: {essay['title']}")
        
        try:
            time.sleep(1)
            response = requests.get(essay['url'])
            essay_soup = BeautifulSoup(response.content, 'html.parser')
            
            content_tags = essay_soup.find_all(['p', 'font'])
            content = '\n\n'.join([tag.get_text().strip() for tag in content_tags if tag.get_text().strip()])
            
            if len(content) > 200:
                essays_data.append({
                    'title': essay['title'],
                    'url': essay['url'],
                    'content': content,
                    'source': 'Paul Graham Essays'
                })
        except Exception as e:
            print(f"Error scraping {essay['title']}: {e}")
            continue
    
    return essays_data

def save_essays(essays_data, output_path='data/raw/essays.json'):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(essays_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {len(essays_data)} essays to {output_path}")

if __name__ == "__main__":
    essays = scrape_pg_essays(max_essays=40)
    save_essays(essays)
