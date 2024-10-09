import pandas as pd
import re
import joblib

model = joblib.load("models/tfidf/model.gz")
tfidf_vectorizer = joblib.load("models/tfidf/tfidf_vectorizer.gz")
rating_mapping = {'G': 0, 'PG': 1, 'M': 2, 'MA15': 3, 'R18': 4}

# Precompile regular expressions for efficiency
newline_pattern = re.compile(r'\n+')
tab_pattern = re.compile(r'\t+')
space_pattern = re.compile(r' +')
screenplay_formatting_pattern = re.compile(r'(FADE IN:|CUT TO:|EXT\.|INT\.|SUPERIMPOSE:)', re.IGNORECASE)
meta_data_pattern = re.compile(r'(written by|&|June \d{1,2}, \d{4})', re.IGNORECASE)
all_caps_pattern = re.compile(r'[A-Z]{2,}(?:\s+[A-Z]{2,})*')

# Function to clean the text
def clean_screenplay_text(text):
    # Replace multiple newlines with a single newline
    text = newline_pattern.sub(' ', text)
    # Replace tabs with a single space
    text = tab_pattern.sub(' ', text)
    # Replace multiple spaces with a single space
    text = space_pattern.sub(' ', text)
    # Remove screenplay formatting (e.g., FADE IN:, CUT TO:, etc.)
    text = screenplay_formatting_pattern.sub('', text)
    # Remove metadata like author names or dates
    text = meta_data_pattern.sub('', text)
    # Remove all caps, typically used for scene descriptions
    text = all_caps_pattern.sub('', text)
    # Remove special characters that are not part of standard sentences
    text = re.sub(r'[^A-Za-z0-9\'\.\?\!,\s]', '', text)
    # Standardize single quotes
    text = re.sub(r'[‘’]', "'", text)
    # Standardize double quotes
    text = re.sub(r'[“”]', '"', text)
    # Remove leading/trailing spaces
    text = text.strip()
    
    return text

# Function to predict the rating of new screenplays
def predict_movie_rating(screenplay):
    print(f"Predicting rating for a new screenplay: '{screenplay[:30]}...'")
    screenplay_cleaned = clean_screenplay_text(screenplay)  # Clean new screenplay
    screenplay_vector = tfidf_vectorizer.transform([screenplay_cleaned])
    rating_index = model.predict(screenplay_vector)[0]
    # Retrieve the rating label from the mapping
    return {v: k for k, v in rating_mapping.items()}[rating_index]

