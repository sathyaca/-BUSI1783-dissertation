# BUSI1783 Dissertation

## Topic
Sentiment Analysis of Trustpilot Reviews Comparing Fast Fashion and Ethical Fashion Brands.

## Brands Included

### Ethical Fashion
- People Tree
- Lucy & Yak
- Rapanui
- Passenger

### Fast Fashion
- ASOS
- Boohoo
- Primark
- Missguided

## Repository Structure

data/
- trustpilot_clean_fixed_final_uk.csv
- trustpilot_raw_corrected.csv

notebooks/
- preprocessing.ipynb

scraper_uk.py

requirements.txt

## Data Collection

Reviews were scraped from Trustpilot using Selenium.

The scraper captures:

- Review text
- Review title
- Star rating
- Review date
- Brand

Company responses were excluded from the final dataset to ensure sentiment analysis reflected customer opinions only.

## Final Dataset

Total Reviews: 1,077+

## Author

MSc Business Analytics Dissertation
