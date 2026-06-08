import requests
import os
import re
from config import DOCS_PATH
from bs4 import BeautifulSoup

# clean html and save to documents folder

SOURCE_URLS = {
    "chicago_maroon": "https://chicagomaroon.com/40981/news/navigating-the-maze-a-guide-to-off-campus-housing/",
    "apartments_com": "https://www.apartments.com/local-guide/off-campus-housing/il/chicago/university-of-chicago/",
    "maroon_housing_life": "https://maroonhousing.com/off-campus-life",
    "maroon_housing_hyde_park": "https://maroonhousing.com/neighborhood-guide/hyde-park",
    "for_rent_university": "https://www.forrentuniversity.com/University-of-Chicago",
    "prked_com": "https://prked.com/post/your-ultimate-guide-to-university-of-chicago-off-campus-housing",
    "casita": "https://www.casita.com/student-accommodation/usa/chicago/university-of-chicago",
    "uhomes": "https://en.uhomes.com/us/chicago/university-of-chicago",
    "domu": "https://www.domu.com/chicago/neighborhoods/hyde-park/apartments-near-university-of-chicago",
    "reddit": "https://old.reddit.com/r/uchicago/comments/1k1uoz3/what_are_some_good_places_to_live/",
    "ugrad_guide": "https://grad.uchicago.edu/admissions/relocating-to-chicago/finding-an-apartment/other-chicago-neighborhoods/",
    "ugrad_apartment_listings": "https://grad.uchicago.edu/admissions/relocating-to-chicago/finding-an-apartment/apartment-listings/",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

STRIP_TAGS = ["script", "style", "nav", "footer", "aside", "form",
              "button", "iframe", "noscript", "svg", "figure", "picture"]

def fetch_html(url) -> str | None:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_text(html) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(STRIP_TAGS):
        tag.decompose()
    
    text = soup.get_text(separator=' ', strip=True)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r"\b(Read more|Share|Subscribe|Sign up|Follow us|Cookie policy|Accept all cookies?)\b", 
                "", text, flags=re.IGNORECASE)
    return text.strip()

def main():
    if not os.path.exists(DOCS_PATH):
        os.makedirs(DOCS_PATH)

    for filename, url in SOURCE_URLS.items():
        html = fetch_html(url)
        if html:
            text = extract_text(html)
            with open(os.path.join(DOCS_PATH, f"{filename}.txt"), 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Saved {filename}.txt")

if __name__ == "__main__":
    main()