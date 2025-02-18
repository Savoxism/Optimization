import os
import requests
from lxml import html

BASE_URL = "https://thuvienphapluat.vn/banan/tin-tuc/tong-hop-72-an-le-da-duoc-cong-bo-o-viet-nam-6712"
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)  

def get_page_content(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, verify=False)  
        response.raise_for_status()  
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

    
# Function to extract all "Án lệ" links from the main page
def extract_links(main_url):
    page_content = get_page_content(main_url)
    if not page_content:
        return []

    tree = html.fromstring(page_content)
    links = []

    # Locate all possible link structures inside the ordered list
    link_elements = tree.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div[3]/div[1]/div/ol/li//a/@href')

    for link in link_elements:
        full_link = link if link.startswith("http") else BASE_URL + link
        links.append(full_link)

    return links

# Function to extract full content from an "Án lệ" page
def extract_case_text(case_url):
    page_content = get_page_content(case_url)
    if not page_content:
        return None

    tree = html.fromstring(page_content)

    # Possible XPaths where the content might be located
    possible_paths = [
        "/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]",
        "/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]",
    ]

    for path in possible_paths:
        content_elements = tree.xpath(path)
        if content_elements:
            return "\n".join([element.text_content().strip() for element in content_elements])

    return None


# Function to save text into a file with sequential numbering
def save_text(index, content):
    if not content:
        print(f"Skipping case {index}, no content found.")
        return

    filename = os.path.join(DATA_DIR, f"{index}.txt")

    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Saved: {filename}")

# Extract links
cases = extract_links(BASE_URL)
print(f"Found {len(cases)} cases.")

# Iterate over links, scrape content, and save with sequential numbering
for i, case_url in enumerate(cases, start=1):
    print(f"Fetching content from: {case_url}")
    case_text = extract_case_text(case_url)
    save_text(i, case_text)

