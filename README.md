# Consumer Sentiment Toward Sustainable Branding in UK Fast Fashion: An NLP-Based Analysis of Trustpilot Reviews

## Overview

This repository contains the code, datasets, and supporting materials for my MSc Business Analytics dissertation.

The study investigates how consumers perceive sustainable branding in the UK fashion industry by analysing Trustpilot reviews using Natural Language Processing (NLP). It compares consumer sentiment and discussion themes between ethical fashion and fast fashion brands to understand how sustainability positioning influences brand trust and perceptions of greenwashing.

---

## Research Questions

* How is consumer sentiment expressed toward sustainable branding claims across UK fashion brands with differing sustainability credentials?
* What thematic patterns of trust or scepticism emerge in consumer discourse, and do these differ significantly between ethical and fast fashion brand categories?

---

## Research Objectives

* Construct an original Trustpilot review corpus covering eight UK fashion brands.
* Apply VADER sentiment analysis to classify consumer sentiment.
* Use BERTopic to identify latent discussion topics.
* Compare sentiment at both brand and category levels.
* Assess whether differences between ethical and fast fashion brands are statistically significant using the Chi-square test.
* Generate insights into consumer perceptions of sustainability, greenwashing, and brand trust.

---

## Brands Analysed

### Ethical Fashion Brands

* Rapanui
* Lucy & Yak
* Finisterre
* Seasalt Cornwall

### Fast Fashion Brands

* ASOS
* Boohoo
* Missguided
* Primark

---

## Methodology

The project follows a multi-stage Natural Language Processing workflow:

1. Data collection from Trustpilot using Selenium.
2. Data cleaning and preprocessing.
3. Sentiment analysis using VADER.
4. Topic modelling using BERTopic.
5. Brand-level and category-level comparisons.
6. Chi-square statistical testing.
7. Interpretation of findings relating to sustainable branding and consumer trust.

---

## Dataset

* **Total reviews:** 1,352
* **Ethical fashion reviews:** 644
* **Fast fashion reviews:** 708

Each review contains:

* Review title
* Review text
* Star rating
* Review date
* Brand
* Brand category

Company responses were removed from the final dataset to ensure that only customer-generated reviews were analysed.

---

## Technologies

* Python
* Selenium
* Pandas
* NumPy
* NLTK
* VADER Sentiment Analysis
* BERTopic
* Sentence Transformers
* UMAP
* HDBSCAN
* SciPy
* Scikit-learn
* Matplotlib

---

## Repository Structure

```text
BUSI1783-dissertation/
│
├── data/
├── notebooks/
├── figures/
├── requirements.txt
├── README.md
└── dissertation.pdf
```

---

## Ethical Considerations

All data were collected from publicly accessible Trustpilot pages. No personally identifiable information was collected, and all analyses were conducted solely for academic research in accordance with university research ethics guidelines.

---

## Author

**Sathya Amaratunge**

MSc Business Analytics

---

## Licence

This repository is intended for academic and educational purposes only.
