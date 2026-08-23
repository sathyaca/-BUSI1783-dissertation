# Consumer Sentiment Toward Sustainable Branding in UK Fast Fashion:
# An NLP-Based Analysis of Trustpilot Reviews

## Overview

This repository contains the code, datasets, analysis outputs and supporting materials for an MSc Business Analytics dissertation.

The study examines consumer sentiment, trust and scepticism across UK fashion brands with contrasting sustainability positioning using 1,352 Trustpilot
reviews. Natural Language Processing (NLP), topic modelling and statistical analysis are used to compare ethical-fashion and fast-fashion brands.

The analysis focuses on consumer sentiment, recurring discussion themes,brand-level differences and the extent to which sustainability-related
terminology appears explicitly in consumer reviews.

---

## Research Questions

1. How is consumer sentiment expressed toward sustainable branding claims across UK fashion brands with differing sustainability credentials?

2. What thematic patterns of trust or scepticism emerge in consumer discourse, and do these differ significantly between ethical and fast-fashion brand
   categories?

---

## Research Objectives

- Construct an original Trustpilot review corpus covering eight UK fashion brands.
- Apply VADER sentiment analysis to classify consumer sentiment.
- Use BERTopic to identify latent discussion topics.
- Compare sentiment at brand and category levels.
- Assess the statistical association between brand category and sentiment
  using the Chi-square test and Cramér's V.
- Examine the frequency of sustainability-related terminology using
  stem-aware regular-expression matching.
- Generate insights into consumer trust, scepticism and sustainable-branding
  discourse.

---

## Brands Analysed

### Ethical Fashion Brands

- Rapanui
- Lucy & Yak
- Finisterre
- Seasalt Cornwall

### Fast Fashion Brands

- ASOS
- Boohoo
- Missguided
- Primark

---

## Dataset

The final corpus contains **1,352 Trustpilot reviews**:

- **Ethical fashion:** 644 reviews
- **Fast fashion:** 708 reviews

The dataset contains review text, star rating, review date, brand and brand
category. Company responses were excluded so that the analysis focused on
customer-generated content.

Review collection periods vary between brands. The `brand_review_date_ranges.csv`
file reports the temporal coverage for each brand and supports transparent
interpretation of this sampling limitation.

---

## Methodology

The project follows the following analytical workflow:

1. Trustpilot review collection using Selenium.
2. Data cleaning and text preprocessing.
3. VADER sentiment analysis.
4. Validation of VADER classifications against star-rating sentiment labels.
5. BERTopic topic modelling.
6. Brand-by-topic and topic-by-sentiment analysis.
7. Chi-square testing and Cramér's V effect-size analysis.
8. Stem-aware sustainability-term frequency analysis.
9. Generation of analytical tables and visualisations.

BERTopic uses Sentence Transformers for document embeddings, UMAP for
dimensionality reduction and HDBSCAN for clustering.

---

## Sustainability-Term Analysis

Sustainability terminology was analysed using stem-aware regular expressions
with word boundaries.

Morphological variants were permitted where appropriate. For example:

- `sustainab*` captures sustainability and sustainable.
- `recycl*` captures recycle, recycled and recycling.
- `environment*` captures environment and environmental.
- `eco` is matched only as the standalone word `eco`.

The standalone treatment of `eco` prevents false matches with unrelated words
such as "recommend", "second", "become" and "economy".

The corrected analysis identified **103 of 1,352 reviews (7.6%)** containing at
least one selected sustainability-related term. **1,249 reviews (92.4%)**
contained none.

The `ethic*` stem was also checked separately for the potentially contradictory
term `unethical`.

---

## Key Findings

- Ethical-fashion reviews were **93.8% positive**.
- Fast-fashion reviews were **65.3% negative**.
- Brand category and sentiment were significantly associated.
- The association had a **large effect size (Cramér's V = 0.643)**.
- BERTopic identified **nine substantive topics**.
- **36.2%** of reviews were classified as BERTopic outliers.
- Consumer discussions primarily concerned product quality, customer service,
  returns, refunds, delivery and shopping experiences.
- Only **103 reviews (7.6%)** contained at least one selected
  sustainability-related term.
- No distinct sustainability-focused topic emerged from BERTopic.
- No reviews contained the `greenwash*` stem.

These findings should not be interpreted as evidence that sustainability
positioning directly caused the observed sentiment differences. The reviews
indicate that trust and scepticism were expressed predominantly through
customer experience, service reliability and product-related discussions.

---

## Repository Structure

```text
BUSI1783-dissertation/
│
├── README.md
├── requirements.txt
│
├── trustpilot_scraper.py
├── preprocessing.py
├── BUSI1783_analysis_corrected.py
├── BUSI1783_analysis_corrected.ipynb
│
├── data/
│   ├── trustpilot_raw_final.csv
│   ├── trustpilot_clean_final.csv
│   └── final_results_corrected.csv
│
├── results/
│   ├── sustainability_term_frequency_corrected.csv
│   ├── brand_review_date_ranges.csv
│   ├── brand_topic_crosstab.csv
│   └── topic_sentiment_percent.csv
│
└── figures/
    ├── rating_distribution.png
    ├── overall_sentiment.png
    ├── sentiment_by_brand.png
    ├── sentiment_by_category.png
    ├── average_vader_by_brand.png
    ├── vader_validation.png
    ├── bertopic_topics.png
    ├── topic_sentiment.png
    └── sustainability_terms_corrected.png
```

---
## Installation

Clone the repository:

```bash
git clone https://github.com/sathyaca/-BUSI1783-dissertation.git
```

Move into the project directory:

```bash
cd ./-BUSI1783-dissertation
```

Install the required packages:

```bash
pip install -r requirements.txt
```

The package versions required to reproduce the analytical environment are provided in `requirements.txt`.

---

## Running the Analysis

The recommended workflow is:

### 1. Data Collection

Run:

```bash
python trustpilot_scraper.py
```

This generates the raw review dataset.

### 2. Data Preprocessing

Run:

```bash
python preprocessing.py
```

This prepares the cleaned corpus used for NLP analysis.

### 3. Main Analysis

Run:

```bash
python BUSI1783_analysis_corrected.py
```

Alternatively, open:

`BUSI1783_analysis_corrected.ipynb`

in Jupyter Notebook or Google Colab and execute the cells sequentially.

### 4. Review Outputs

Final analytical outputs are stored in:

- `results/`
- `figures/`


---


## Methodological Limitations

Several limitations should be considered when interpreting the repository outputs.

First, the corpus contains Trustpilot reviews only and therefore may not represent consumer discourse on other platforms.

Second, temporal coverage differs substantially between brands. In particular, Seasalt Cornwall's 178 reviews cover only a three-day period. Brand-level comparisons may consequently be influenced by temporal sampling effects.

Third, VADER is lexicon-based and may not fully identify sarcasm, contextual language or complex sentiment.

Fourth, BERTopic classified 36.2% of the corpus as outliers, reflecting considerable linguistic heterogeneity.

Finally, the study is observational. Statistical associations between brand category and sentiment should not be interpreted as proof that sustainability positioning or perceived greenwashing caused the observed sentiment differences.

---
## Ethical Considerations

The study used publicly accessible Trustpilot review data for academic research.

No personally identifiable reviewer information was intentionally retained in the analytical dataset. Company responses were excluded so that the analysis focused on customer-generated review content.

The research and associated data handling were conducted for academic purposes in accordance with the applicable university research ethics requirements.


---
## Author

**Sathya Amaratunge**  
MSc Business Analytics

---

## Academic Purpose

This repository was developed as supporting material for an MSc Business Analytics dissertation and is intended primarily for academic assessment, research transparency and educational purposes.

---

## Licence

This repository is intended for academic and educational use. Any reuse of the code, data or analytical outputs should appropriately acknowledge the original project and comply with the terms and conditions of the underlying data source.
