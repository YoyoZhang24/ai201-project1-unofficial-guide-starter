import requests
from config import DOCS_PATH
from bs4 import BeautifulSoup


SOURCE_URLS = {
    "chicago_maroon": "https://chicagomaroon.com/40981/news/navigating-the-maze-a-guide-to-off-campus-housing/",
    "apartments_coom": "https://www.apartments.com/off-campus-housing/il/chicago/university-of-chicago/",
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

# clean html and save to documents folder

def fetch_html(url) -> str | None:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_text(html) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    for element in soup(['nav', 'footer', 'header', 'aside', 'script', 'style']):
        element.decompose()
    return soup.get_text(separator='\n', strip=True)

def __main__():
    for filename, url in SOURCE_URLS.items():
        html = fetch_html(url)
        if html:
            text = extract_text(html)
            with open(os.path.join(DOCS_PATH, f"{filename}.txt"), 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Saved {filename}.txt")

if __name__ == "__main__":
    __main__()