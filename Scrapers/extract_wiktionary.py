import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

visited_urls = set()
current_id = 1  # Start the ID counter

# Initialize Selenium WebDriver
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_service = Service('/opt/homebrew/bin/chromedriver')  # Update with the path to your ChromeDriver
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    print("Initialized WebDriver")
    return driver

# Function to log in to Wiktionary
def login_to_wiktionary(driver, username, password):
    driver.get("https://en.wiktionary.org/w/index.php?title=Special:UserLogin")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "wpName")))

    username_field = driver.find_element(By.NAME, "wpName")
    password_field = driver.find_element(By.NAME, "wpPassword")
    login_button = driver.find_element(By.NAME, "wploginattempt")

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pt-userpage")))
    print(f"Logged in as {username}")

# Extract links for each lemma in the category
def extract_lemma_links(base_url):
    lemma_links = []
    subcategory_links = []

    while base_url:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract lemma links from the current page
        links = soup.select("div.mw-category-group a[href^='/wiki/Reconstruction:Proto-Semitic/']")
        lemma_links.extend([urljoin("https://en.wiktionary.org", link['href']) for link in links])

        # Extract subcategory links from the current page
        subcategory_links.extend([urljoin("https://en.wiktionary.org", a['href'])
                                  for a in soup.select("div#mw-subcategories a[href*='Category:Proto-Semitic_lemmas']")])

        print(f"Found {len(links)} lemma links on page {base_url}")

        next_page = soup.select_one("a[title='Category:Proto-Semitic lemmas'][href*='pagefrom']")
        base_url = urljoin("https://en.wiktionary.org", next_page['href']) if next_page else None

    # Process subcategories
    for subcategory in subcategory_links:
        print(f"Processing subcategory: {subcategory}")
        lemma_links.extend(extract_lemma_links(subcategory))

    print(f"Total lemma links extracted: {len(lemma_links)}")
    return lemma_links

# Function to extract the first relevant English link for Proto-Semitic roots
def extract_proto_semitic_concept(soup):
    # Find the first link with #English
    english_link = soup.find('a', href=lambda href: href and '#English' in href)
    
    if english_link:
        return english_link.get_text(strip=True)
    
    return "Unknown"

# Function to extract the word type from Proto-Semitic roots
def extract_proto_semitic_word_type(soup):
    word_types = set()  # Use a set to avoid duplicates

    # Find all possible word type headings like "Noun", "Verb", etc.
    for heading in soup.find_all(['h3', 'h4']):
        if heading.get_text(strip=True) in ["Noun", "Verb", "Adjective", "Pronoun"]:
            word_types.add(heading.get_text(strip=True))

    return list(word_types) if word_types else ["None"]

# Function to extract the first relevant English link from a descendant's page after navigating to it
def extract_translation_from_descendant_page(driver, url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the first link with #English
    english_link = soup.find('a', href=lambda href: href and '#English' in href)
    if english_link:
        return english_link.get_text(strip=True)
    
    # Consider a fallback strategy to check for other links or elements
    alt_concept = soup.find('span', {'class': 'mention-gloss'})
    if alt_concept:
        return alt_concept.get_text(strip=True)

    return "Unknown"

# Extract word details from a lemma page
def extract_details_from_lemma_page(driver, url, output_file):
    global current_id

    if url in visited_urls:
        return
    visited_urls.add(url)

    print(f"Processing lemma page: {url}")

    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    lemma = soup.find("h1", id="firstHeading").get_text(strip=True)
    group_value = lemma.split("/")[-1]  # The group value is based on the lemma name
    cogid = current_id  # Use the current ID for the Proto-Semitic root
    current_id += 1  # Increment the ID counter

    # Extract the concept specifically for the Proto-Semitic root
    concept = extract_proto_semitic_concept(soup)
    
    # Extract the word type for the Proto-Semitic root
    word_types = extract_proto_semitic_word_type(soup)
    word_type_str = ", ".join(set(word_types)) if word_types else "None"

    # Save the Proto-Semitic root itself with the extracted concept and word type
    save_to_file(cogid, cogid, "Proto-Semitic", group_value, group_value, concept, word_type_str, output_file)
    print(f"Saved Proto-Semitic root: {group_value} with COGID: {cogid}, CONCEPT: {concept}, and WORD_TYPE: {word_type_str}")

    # Process descendants by the doculect
    process_descendants(driver, soup, cogid, output_file)

# Function to process descendants recursively by the doculect
def process_descendants(driver, soup, cogid, output_file):
    descendants_section = soup.find('h4', string="Descendants")
    if descendants_section:
        ul = descendants_section.find_next('ul')
        if ul:
            process_descendants_recursive(ul, cogid, output_file, driver)

def process_descendants_recursive(element, cogid, output_file, driver):
    global current_id

    for li in element.find_all('li', recursive=False):
        if li.find('ul'):  # If the <li> has a nested <ul>, process it recursively
            process_descendants_recursive(li.find('ul'), cogid, output_file, driver)
        else:
            doculect_element = li.find(string=True, recursive=False)
            if doculect_element is None:
                print("No valid DOCULECT found, skipping...")
                continue

            doculect = doculect_element.strip().strip(':')
            print(f"Found DOCULECT: {doculect}")

            descendant_links = li.find_all('a', href=True)
            for link in descendant_links:
                word_url = urljoin("https://en.wiktionary.org", link['href'])
                form = link.get_text(strip=True)  # Original form of the word (from link text)

                # Navigate to the descendant's page to extract the first relevant English translation (concept)
                concept = extract_translation_from_descendant_page(driver, word_url)

                # Extract word type from the descendant's page, selecting the first one under the doculect
                driver.get(word_url)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                descendant_soup = BeautifulSoup(driver.page_source, 'html.parser')
                word_types = extract_proto_semitic_word_type(descendant_soup)
                word_type_str = word_types[0] if word_types else "None"  # Select the first word type

                # Assuming the transliteration is in the next span with 'lang' attribute
                value_span = link.find_next('span', {'class': 'Latn'})
                value = value_span.get_text(strip=True) if value_span else "N/A"  # Extract the English transliteration

                # Skip saving if the DOCULECT is English
                if doculect.lower() == "english":
                    print(f"Skipping English word: {form}")
                    continue

                print(f"Processing word: {form} (transliterated: {value}) from {doculect} with CONCEPT: {concept} and WORD_TYPE: {word_type_str}")
                save_to_file(current_id, cogid, doculect, value, form, concept, word_type_str, output_file)
                current_id += 1
                
# Save extracted details to CSV with headers
def save_to_file(id, cogid, doculect, value, form, concept, word_type, output_file):
    with open(output_file, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # Write headers if the file is empty
        if f.tell() == 0:
            writer.writerow(["ID", "COGID", "DOCULECT", "VALUE", "FORM", "CONCEPT", "WORD_TYPE"])  # Added WORD_TYPE header
        writer.writerow([id, cogid, doculect, value, form, concept, word_type])  # Populate CONCEPT and WORD_TYPE with extracted values
   
    print(f"Data saved: ID: {id}, COGID: {cogid}, DOCULECT: {doculect}, VALUE: {value}, FORM: {form}, CONCEPT: {concept}, WORD_TYPE: {word_type}")

# Start crawling and extract all necessary details
def start_crawling(base_url, username, password, output_file):
    driver = initialize_driver()
    login_to_wiktionary(driver, username, password)

    lemma_links = extract_lemma_links(base_url)
    
    for url in lemma_links:
        extract_details_from_lemma_page(driver, url, output_file)

    driver.quit()

def main():
    base_url = "https://en.wiktionary.org/wiki/Category:Proto-Semitic_lemmas"
    output_file = "proto_semitic_words.csv"
    username = "Your UserName"
    password = "Your Password"

    # Clear the output file and write headers, including WORD_TYPE and CONCEPT
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "COGID", "DOCULECT", "VALUE", "FORM", "CONCEPT", "WORD_TYPE"])  # Added WORD_TYPE header

    start_crawling(base_url, username, password, output_file)
    print(f"Crawling completed for {base_url}")

if __name__ == "__main__":
    main()
