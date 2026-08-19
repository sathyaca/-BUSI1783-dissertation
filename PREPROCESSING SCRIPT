# ============================================================
# PREPROCESSING SCRIPT
# BUSI1783 — Sathya Charith Amaratunge
# Tokenisation, stopword removal, lemmatisation
# ============================================================

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

# Load RAW file — pre-deduplication scrape output
df = pd.read_csv('trustpilot_raw_final.csv')

print(f"Raw reviews loaded: {len(df)}")
print(f"Columns: {df.columns.tolist()}")

before_dedup = len(df)
df = df.drop_duplicates(subset=['Text'])
print(f"Removed {before_dedup - len(df)} duplicates")

# Remove short reviews
df = df[df['Text'].str.len() > 20]

# Remove truncated See more artefacts
df = df[~df['Text'].str.contains('See more', case=False, na=False)]

# Convert date and rating
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df = df.dropna(subset=['Rating'])

print(f"After cleaning: {len(df)} reviews")
print(f"Missing ratings: {df['Rating'].isna().sum()}")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    # Lowercase
    text = str(text).lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    # Remove special characters and numbers
    text = re.sub(r'[^a-z\s]', '', text)
    # Tokenise
    tokens = word_tokenize(text)
    # Remove stopwords
    tokens = [t for t in tokens if t not in stop_words]
    # Lemmatise — default noun POS tag
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return ' '.join(tokens)

print("\nApplying preprocessing pipeline...")
df['Clean_Text'] = df['Text'].apply(preprocess)
print("Preprocessing complete")

df.to_csv('trustpilot_clean_final.csv', index=False)
print(f"\nClean file saved: {len(df)} reviews")
print(df[['Brand', 'Text', 'Clean_Text']].head())
