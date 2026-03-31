import requests
from textblob import TextBlob
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Emily Dickinson Poem Analysis")

# Starting words for each emotion
emotions = {
    "sad": ["sad", "grief", "cry", "lonely", "hopeless", "miserable", "pain", "loss", "despair", "broken", "mourn", "empty", "regret", "suffer", "tears", "heartbreak", "abandoned", "gloomy", "woe", "lament"],
    "happy": ["happy", "joy", "smile", "laugh", "love", "bright", "cheer", "bliss", "celebrate", "grateful", "harmony", "delight", "hope", "radiant", "playful", "serene", "content", "elated", "jubilant", "merry"],
    "fear": ["fear", "scared", "panic", "dread", "horror", "tremble", "threat", "anxiety", "phobia", "eerie", "foreboding", "menace", "peril", "sinister", "terror", "uneasy", "vulnerable", "wary", "shock", "paranoid"],
    "anger": ["angry", "rage", "hate", "fury", "hostile", "bitter", "conflict", "defiant", "fierce", "grudge", "harsh", "jealous", "livid", "outrage", "provoke", "quarrel", "rebel", "savage", "temper", "wrath"],
    "surprise": ["surprise", "shock", "astonish", "amaze", "startle", "wonder", "stun", "astound", "bewilder", "unexpected", "sudden", "gasp", "remarkable", "extraordinary", "bizarre", "curious", "unbelievable", "marvel", "jolt", "awe"],
    "disgust": ["disgust", "revolting", "repulsive", "vile", "gross", "nasty", "foul", "loathe", "detest", "abhor", "nauseate", "sickening", "hideous", "repel", "despise", "offensive", "filthy", "putrid", "horrid", "appalling"],
}

# Fetch all Emily Dickinson poems from PoetryDB and compute polarity with TextBlob
poems = requests.get("https://poetrydb.org/author/Emily Dickinson").json()
df = pd.DataFrame([{"title": p['title'], "text": "\n".join(p['lines']), "polarity": TextBlob("\n".join(p['lines'])).sentiment.polarity} for p in poems])

# Expand each emotion's word list with synonyms from the Free Dictionary API
emotion_words = {}
for emotion, words in emotions.items():
    expanded = set(words)
    for word in words:
        r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if r.status_code == 200:
            for entry in r.json():
                for meaning in entry.get("meanings", []):
                    expanded.update(meaning.get("synonyms", []))
                    for d in meaning.get("definitions", []):
                        expanded.update(d.get("synonyms", []))
    emotion_words[emotion] = expanded

# Count how many emotion words appear in each poem
def count_emotions(text):
    words = text.lower().split()
    return {e: sum(1 for w in words if w in ws) for e, ws in emotion_words.items()}

emotion_df = df['text'].apply(count_emotions).apply(pd.Series)
emotion_df[['title', 'text']] = df[['title', 'text']].values

# Polarity histogram
st.subheader("Polarity Distribution")
fig, ax = plt.subplots()
df['polarity'].plot(kind='hist', bins=30, edgecolor='black', ax=ax)
st.pyplot(fig)

# Emotion word frequency bar chart across all poems
st.subheader("Emotion Word Frequency")
fig2, ax2 = plt.subplots()
emotion_df.drop(columns=['title','text']).sum().plot(kind='bar', edgecolor='black', ax=ax2)
ax2.set_xticklabels(emotion_words.keys(), rotation=45)
st.pyplot(fig2)

# Poem with the highest emotion word count for each category
st.subheader("Top Poem per Emotion")
for emotion in emotions:
    top = emotion_df.nlargest(1, emotion).iloc[0]
    st.markdown(f"### {emotion.capitalize()} — **{top['title']}** ({int(top[emotion])} matches)")
    st.text(top['text'])

# 5 most positive and negative poems by polarity score
for label, fn in [("5 Most Positive", df.nlargest), ("5 Most Negative", df.nsmallest)]:
    st.subheader(label)
    for _, row in fn(5, 'polarity').iterrows():
        st.markdown(f"**{row['title']}** ({row['polarity']:.2f})")
        st.text(row['text'])

# Full poem dataframe with polarity scores
st.subheader("All Poems")
st.dataframe(df[['title', 'polarity']])

# Full expanded emotion word list
st.subheader("Emotion Word Lists")
st.dataframe(pd.DataFrame([(e, w) for e, ws in emotion_words.items() for w in ws], columns=["emotion", "word"]))

st.subheader("Write Up")
st.markdown("""
This project analyzes the emotional and sentimental content of Emily Dickinson's poetry using natural language processing tools (TextBlob) and a custom emotion lexicon.
            
Emily Dickinson (1830–1886) was an American poet known for her unconventional style, use of slant rhyme, and deeply introspective themes. She wrote nearly 1,800 poems, most of which were published posthumously. Her work frequently explores themes of death, immortality, nature, and the inner life, making her an ideal subject for sentiment analysis. I enjoy the ephemeral quality of her poetry.

Poems were fetched from the PoetryDB API. Polarity scores were computed using TextBlob, which assigns each poem a score from -1 (most negative) to +1 (most positive). A custom emotion lexicon was built for six emotions — sad, happy, fear, anger, surprise, and disgust, using 20 starting words per emotion, expanded with synonyms from the Free Dictionary API. Each poem was then scanned for matches against these word lists.

The polarity histogram shows that most of Dickinson's poems cluster slightly above neutral, at around 0.1, suggesting a restrained but generally contemplative tone. The emotion bar chart reveals that sadness and happiness dominate her vocabulary, while disgust is the least represented. The top poems per emotion confirm recurring themes of mortality (fear), longing (sad), and spiritual wonder (surprise).

**Key Takeaways**
- Dickinson's poetry leans melancholic but rarely reaches extreme negativity
- Sadness is her most emotionally loaded category
- Words associated with wonder and surprise appear frequently, reflecting her fascination with the unknown
- TextBlob polarity alone understates the emotional complexity, where the emotion lexicon reveals nuance that sentiment scores miss. Both are still unable to truely capture the depth of her work, but together they provide a richer picture of her emotional landscape across her poetry.
""")