# ============================================================
# TRUSTPILOT SCRAPER 
# Data Collection
# Ethical Fashion vs Fast Fashion
# ============================================================

import pandas as pd
import time
import re
import random
import nltk
import matplotlib.pyplot as plt

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException

from webdriver_manager.chrome import ChromeDriverManager

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

brands = {


    'People Tree': 'www.peopletree.co.uk',
    'Lucy & Yak': 'www.lucyandyak.com',
    'Rapanui': 'rapanuiclothing.com',
    'Passenger': 'www.passenger-clothing.com',



    'Oh Polly': 'www.ohpolly.com',
    'ASOS': 'www.asos.com',
    'Boohoo': 'www.boohoo.com',
    'Cotton Traders': 'www.cottontraders.com'
}



options = Options()

# Run browser invisibly
options.add_argument("--headless=new")

options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")

options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/137.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.set_page_load_timeout(60)



def scrape_trustpilot(brand_name, brand_slug, max_pages=120):

    collected = []
    seen_reviews = set()

    for page in range(1, max_pages + 1):

        url = f"https://www.trustpilot.com/review/{brand_slug}?page={page}"

        print("\n================================================")
        print(f"{brand_name} | PAGE {page}")
        print(url)

        try:

            driver.get(url)

            # Random delay to reduce blocking
            time.sleep(random.uniform(4, 7))

            # Scroll page
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            time.sleep(3)

            reviews = driver.find_elements(By.TAG_NAME, "article")

            print(f"Found {len(reviews)} reviews")

            # Stop if no reviews found
            if len(reviews) == 0:

                print("No more reviews found.")
                break

            page_reviews = 0

            for review in reviews:

                try:

                

                    text = ""

                    paragraphs = review.find_elements(By.TAG_NAME, "p")

                    if len(paragraphs) > 0:
                        text = paragraphs[-1].text.strip()

                    text = str(text).strip()

                    if len(text) < 20:
                        continue

                    # Remove duplicates
                    if text in seen_reviews:
                        continue

                    seen_reviews.add(text)

            

                    title = ""

                    try:

                        titles = review.find_elements(By.TAG_NAME, "h2")

                        if len(titles) > 0:
                            title = titles[0].text.strip()

                    except:
                        pass

        

                    rating = None

                    try:

                        rating_element = review.find_element(
                            By.XPATH,
                            ".//div[contains(@data-service-review-rating,'')]"
                        )

                        rating = rating_element.get_attribute(
                            "data-service-review-rating"
                        )

                    except:
                        pass

                  

                    date = None

                    try:

                        time_element = review.find_element(
                            By.TAG_NAME,
                            "time"
                        )

                        date = time_element.get_attribute(
                            "datetime"
                        )

                    except:
                        pass

    

                    if brand_name in [
                        'People Tree',
                        'Lucy & Yak',
                        'Rapanui',
                        'Passenger'
                    ]:

                        category = 'Ethical Fashion'

                    else:

                        category = 'Fast Fashion'

                

                    collected.append({
                        'brand': brand_name,
                        'category': category,
                        'title': title,
                        'text': text,
                        'rating': rating,
                        'date': date,
                        'source': 'trustpilot'
                    })

                    page_reviews += 1

                except Exception as e:

                    print("Review extraction error:", e)

            print(f"Collected from page: {page_reviews}")
            print(f"Total collected so far: {len(collected)}")

       
            if page_reviews < 3:

                print("Very few new reviews found. Ending scraper.")
                break

            # Delay between pages
            time.sleep(random.uniform(2, 5))

        except TimeoutException:

            print("Timeout occurred. Retrying...")
            continue

        except Exception as e:

            print("Page error:", e)

    return collected



all_data = []

for brand_name, brand_slug in brands.items():

    print("\n################################################")
    print(f"SCRAPING BRAND: {brand_name}")
    print("################################################")

    reviews = scrape_trustpilot(
        brand_name,
        brand_slug,
        max_pages=120
    )

    all_data.extend(reviews)

    print(f"\nFinished {brand_name}")
    print(f"Collected: {len(reviews)} reviews")

    # Pause between brands
    time.sleep(random.uniform(5, 10))


driver.quit()



df = pd.DataFrame(all_data)

print("\n================================================")
print(f"TOTAL RAW REVIEWS: {len(df)}")
print("================================================")

if len(df) == 0:

    print("No reviews collected.")
    exit()

print("\nCleaning dataset...")

# Remove duplicates
df = df.drop_duplicates(subset=['text'])

# Remove short reviews
df = df[df['text'].str.len() > 20]

# Convert date column
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Convert rating column
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')



df = df.sort_values(by='date', ascending=False)

print(f"Reviews after cleaning: {len(df)}")

raw_path = r'C:\Users\LENOVO\Desktop\trustpilot_raw_max_reviews.csv'

df.to_csv(raw_path, index=False)

print(f"\nRaw data saved:\n{raw_path}")

lemmatizer = WordNetLemmatizer()

stop_words = set(stopwords.words('english'))

def preprocess(text):

    text = str(text).lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Remove punctuation and numbers
    text = re.sub(r'[^a-z\s]', '', text)

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords + lemmatize
    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word not in stop_words
    ]

    return ' '.join(tokens)

print("\nPreprocessing text...")

df['clean_text'] = df['text'].apply(preprocess)

print("Preprocessing complete.")


clean_path = r'C:\Users\LENOVO\Desktop\trustpilot_clean_max_reviews.csv'

df.to_csv(clean_path, index=False)

print(f"\nClean data saved:\n{clean_path}")
print("\nReviews by category:\n")
print(df['category'].value_counts())
print("\nDate Range Summary:\n")
print("Earliest Review:", df['date'].min())
print("Latest Review:", df['date'].max())
print("\n================================================")
print("SCRAPING COMPLETE")
print(f"FINAL DATASET SIZE: {len(df)} REVIEWS")
print("================================================")