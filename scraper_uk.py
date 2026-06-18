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

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("wordnet")


brands = {
    # Ethical Fashion
    "People Tree": "www.peopletree.co.uk",
    "Lucy & Yak": "www.lucyandyak.com",
    "Rapanui": "rapanuiclothing.com",
    "Passenger": "www.passenger-clothing.com",

    # Fast Fashion
    "Primark": "www.primark.com",
    "ASOS": "www.asos.com",
    "Boohoo": "www.boohoo.com",
    "Missguided": "www.missguided.co.uk"
}

ethical_brands = ["People Tree", "Lucy & Yak", "Rapanui", "Passenger"]


options = Options()
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

def extract_rating(review):
    try:
        elements = review.find_elements(By.XPATH, ".//*[@data-service-review-rating]")
        for element in elements:
            rating = element.get_attribute("data-service-review-rating")
            if rating and rating.isdigit():
                return int(rating)
    except:
        pass

    try:
        images = review.find_elements(By.TAG_NAME, "img")
        for img in images:
            alt = img.get_attribute("alt")
            if alt:
                match = re.search(r"Rated\s+(\d+)\s+out of\s+5", alt)
                if match:
                    return int(match.group(1))
    except:
        pass

    try:
        elements = review.find_elements(By.XPATH, ".//*[@aria-label]")
        for element in elements:
            label = element.get_attribute("aria-label")
            if label:
                match = re.search(r"Rated\s+(\d+)\s+out of\s+5", label)
                if match:
                    return int(match.group(1))
    except:
        pass

    return None


def extract_customer_review_text(review):
    """
    Extracts customer review text only.
    Removes company reply blocks before extracting paragraph text.
    """

    html = review.get_attribute("outerHTML")
    soup = BeautifulSoup(html, "html.parser")

    # Remove company/business reply blocks
    for tag in soup.find_all(True):

        tag_info = " ".join([
            str(tag.get("class")),
            str(tag.get("id")),
            str(tag.get("data-service-review-business-reply")),
            str(tag.get("data-business-unit-reply"))
        ]).lower()

        if "reply" in tag_info or "business-unit" in tag_info:
            tag.decompose()

    candidates = []

    # Preferred Trustpilot selectors
    preferred_selectors = [
        "p[data-service-review-content-paragraph]",
        "p[data-service-review-text-typography]"
    ]

    for selector in preferred_selectors:
        for p in soup.select(selector):
            text = p.get_text(" ", strip=True)
            if text:
                candidates.append(text)

    # Fallback: all paragraph text after removing company replies
    if not candidates:
        for p in soup.find_all("p"):
            text = p.get_text(" ", strip=True)
            if text:
                candidates.append(text)

    cleaned_candidates = []

    bad_phrases = [
        "date of experience",
        "thank you for your review",
        "thanks for your review",
        "thank you for taking the time",
        "we are sorry",
        "we're sorry",
        "please contact",
        "kind regards",
        "best regards",
        "customer service team",
        "customer care team",
        "we have requested",
        "we would like to look into this",
        "we’re sorry",
        "we apologise",
        "we apologize"
    ]

    for text in candidates:
        text = str(text).strip()

        if text == "" or len(text) < 20:
            continue

        if "see more" in text.lower():
            continue

        if any(phrase in text.lower() for phrase in bad_phrases):
            continue

        cleaned_candidates.append(text)

    if cleaned_candidates:
        return cleaned_candidates[0]

    return ""



def scrape_trustpilot(brand_name, brand_slug, max_pages=150):

    collected = []
    seen_reviews = set()
    weak_pages = 0

    for page in range(1, max_pages + 1):

        url = f"https://www.trustpilot.com/review/{brand_slug}?page={page}"

        print("\n================================================")
        print(f"{brand_name} | PAGE {page}")
        print(url)

        try:
            driver.get(url)
            time.sleep(random.uniform(4, 7))

            for pos in [800, 1600, 2400, 3200]:
                driver.execute_script(f"window.scrollTo(0, {pos});")
                time.sleep(1)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            reviews = driver.find_elements(By.TAG_NAME, "article")
            print(f"Found {len(reviews)} review containers")

            if len(reviews) == 0:
                print("No reviews found. Stopping this brand.")
                break

            page_reviews = 0

            for review in reviews:
                try:
                    text = extract_customer_review_text(review)
                    text = str(text).strip()

                    if text == "" or len(text) < 20:
                        continue

                    if text in seen_reviews:
                        continue

                    seen_reviews.add(text)

                    title = ""
                    try:
                        titles = review.find_elements(By.TAG_NAME, "h2")
                        if titles:
                            title = titles[0].text.strip()
                    except:
                        pass

                    rating = extract_rating(review)

                    if rating is None:
                        continue

                    date = None
                    try:
                        time_element = review.find_element(By.TAG_NAME, "time")
                        date = time_element.get_attribute("datetime")
                    except:
                        pass

                    category = (
                        "Ethical Fashion"
                        if brand_name in ethical_brands
                        else "Fast Fashion"
                    )

                    collected.append({
                        "Brand": brand_name,
                        "Category": category,
                        "Title": title,
                        "Text": text,
                        "Rating": rating,
                        "Date": date,
                        "Source": "Trustpilot"
                    })

                    page_reviews += 1

                except Exception as e:
                    print("Review extraction error:", e)

            print(f"Collected this page: {page_reviews}")
            print(f"Total collected for {brand_name}: {len(collected)}")

            if page_reviews < 3:
                weak_pages += 1
            else:
                weak_pages = 0

            if weak_pages >= 3:
                print("Several weak pages found. Stopping this brand.")
                break

            time.sleep(random.uniform(2, 5))

        except TimeoutException:
            print("Timeout occurred. Moving to next page.")
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
        brand_name=brand_name,
        brand_slug=brand_slug,
        max_pages=150
    )

    all_data.extend(reviews)

    print(f"Finished {brand_name}: {len(reviews)} reviews")

    time.sleep(random.uniform(6, 12))

driver.quit()

df = pd.DataFrame(all_data)

print("\n================================================")
print(f"TOTAL RAW REVIEWS: {len(df)}")
print("================================================")

if len(df) == 0:
    print("No reviews collected.")
    exit()



df = df.drop_duplicates(subset=["Text"])
df = df[df["Text"].str.len() > 20]

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

df = df.dropna(subset=["Rating"])
df = df.sort_values(by="Date", ascending=False)

print(f"Reviews after cleaning: {len(df)}")
print("Missing ratings:", df["Rating"].isna().sum())


raw_path = r"D:\proposal\trustpilot_raw_corrected.csv"
df.to_csv(raw_path, index=False)


lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess(text):

    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)

    tokens = word_tokenize(text)

    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word not in stop_words
    ]

    return " ".join(tokens)

df["Clean_Text"] = df["Text"].apply(preprocess)



clean_path = r"D:\proposal\trustpilot_clean_corrected.csv"
df.to_csv(clean_path, index=False)


print("\nReviews per brand:")
print(df["Brand"].value_counts())

print("\nReviews by category:")
print(df["Category"].value_counts())

print("\nRating availability:")
print(df["Rating"].value_counts(dropna=False).sort_index())

print("\nDate range by brand:")
print(df.groupby("Brand")["Date"].agg(["min", "max", "count"]))

print("\nTruncated reviews remaining:")
print(df["Text"].str.contains("See more", case=False, na=False).sum())

print("\nPossible company replies remaining:")
reply_check = df["Text"].str.contains(
    "thank you for your review|thanks for your review|kind regards|customer service team|customer care team|please contact|we are sorry|we're sorry",
    case=False,
    na=False
).sum()
print(reply_check)

plt.figure(figsize=(12, 6))
df["Brand"].value_counts().plot(kind="bar")

plt.title("Reviews per Brand")
plt.xlabel("Brand")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=45)
plt.tight_layout()

plot_path = r"D:\proposal\summary_corrected.png"
plt.savefig(plot_path)
plt.show()

print(f"\nRaw file saved to: {raw_path}")
print(f"Clean file saved to: {clean_path}")
print(f"Graph saved to: {plot_path}")

print("\n================================================")
print("SCRAPING COMPLETE")
print(f"FINAL DATASET SIZE: {len(df)} REVIEWS")
print("================================================")
