# Emily Dickinson Poem Analysis

A Streamlit web app that analyzes the emotional and sentimental content of Emily Dickinson's poetry using natural language processing and a custom emotion lexicon.

## About

Emily Dickinson (1830–1886) wrote nearly 1,800 poems exploring themes of death, immortality, nature, and the inner life. This project fetches her complete works from the PoetryDB API and examines them through two lenses:

- **Sentiment polarity** via TextBlob, scoring each poem from -1 (most negative) to +1 (most positive)
- **Emotion word frequency** using a custom lexicon covering six emotions — sadness, happiness, fear, anger, surprise, and disgust — expanded with synonyms from the Free Dictionary API

## Features

- **Polarity histogram** showing the distribution of sentiment across all poems
- **Emotion word frequency chart** comparing how often each emotion category appears
- **Top poem per emotion** highlighting the most emotionally loaded poem in each category
- **Most positive and negative poems** ranked by TextBlob polarity score
- **Searchable dataframe** of all poems with their polarity scores
- **Full emotion word lists** showing every term in the expanded lexicon

## How It Works

1. All Emily Dickinson poems are fetched from the [PoetryDB API](https://poetrydb.org)
2. Each poem receives a polarity score from TextBlob's sentiment analyzer
3. A base lexicon of 20 words per emotion is expanded using synonyms from the [Free Dictionary API](https://dictionaryapi.dev)
4. Each poem is scanned for matches against the expanded word lists
5. Results are displayed as interactive charts and tables in Streamlit

## Deployment

This app is configured for [Streamlit Community Cloud](https://streamlit.io/cloud). Push to the `main` branch and it will deploy automatically.

## Dependencies

- `streamlit` — web app framework
- `textblob` — sentiment analysis
- `pandas` — data manipulation
- `matplotlib` — charts and visualizations
- `requests` — API calls to PoetryDB and Free Dictionary

## Pros & Cons

### Pros

- **Dual-method analysis** — combining TextBlob polarity with a custom emotion lexicon gives a richer picture than either approach alone
- **Automated synonym expansion** — using the Free Dictionary API to grow the base word lists improves coverage without manual curation
- **Reproducible** — all data comes from public APIs, so anyone can run this and get the same results
- **Broad coverage** — analyzes Dickinson's full body of work rather than a curated subset, avoiding selection bias

### Cons

- **No context awareness** — bag-of-words matching can't handle negation ("not happy"), irony, or metaphor, all of which are central to Dickinson's style
- **TextBlob's training data mismatch** — the sentiment model was trained on product reviews, not 19th-century poetry, so polarity scores are a rough proxy
- **Synonym drift** — expanded word lists may include loosely related terms that don't actually convey the intended emotion, introducing noise
- **No lemmatization** — inflected forms like "mourning" or "feared" won't match base words like "mourn" or "fear" unless they happen to appear in the synonym expansion
- **Performance** — hundreds of dictionary API calls are made on every app load with no caching, leading to slow startup times

## Key Findings

- Dickinson's poetry leans melancholic but rarely reaches extreme negativity, with most poems clustering around a polarity of 0.1
- Sadness is the most emotionally loaded category across her work
- Words associated with wonder and surprise appear frequently, reflecting her fascination with the unknown
- TextBlob polarity alone understates the emotional complexity — the emotion lexicon reveals nuance that sentiment scores miss
