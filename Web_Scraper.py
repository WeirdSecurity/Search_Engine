import urllib.robotparser
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import Inverted_Indexing
from collections import deque  
import time


def scrape(url):
    try:
        req = Request(url, headers={'User-Agent': 'MySearchEngineBot/1.0'})
        with urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            return BeautifulSoup(html_content, 'html.parser')
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
    return None


def get_links(soup, base_url):
    links = set() 
    if soup is None:
        return []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            absolute_url = urljoin(base_url, href)
            links.add(absolute_url)
    return list(links)

def get_metadata(soup):
    if soup is None:
        return "No Title", ""

    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else "No Title"
    snippet = ""
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    
    if meta_desc and meta_desc.get('content'):
        snippet = meta_desc.get('content').strip()
        
    if not snippet:
        text = soup.get_text(separator=' ', strip=True)
        snippet = text[:150] + "..." if len(text) > 150 else text
        
    return title, snippet

def get_content(soup):

    if soup is None:
        return ""
    text = soup.get_text()
    return text


def crawl(seed_url, max_pages=10):
    index = Inverted_Indexing.NLTKInvertedIndex()
    index.load_index()
    queue = deque([seed_url])
    visited = set()
    page_popleft = 0
    
    while queue and page_popleft < max_pages:
        url = queue.popleft()
        if url in visited:
            continue

        print(f"[{page_popleft + 1}/{max_pages}] Crawling: {url}")

        soup = scrape(url)
        if soup:
            title, snippet = get_metadata(soup)
            index.add_metadata(url, title, snippet)
            index.add_document(url, get_content(soup))
            for link in get_links(soup,url):
                if link not in visited:
                    queue.append(link)

            visited.add(url)
            page_popleft +=1
            time.sleep(1)

    index.save_index()

if __name__ == "__main__":
    url = input("Enter the URL to crawl: ")
    crawl(url, max_pages=100)



