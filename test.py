import time
import csv
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from twitter_client import get_recent_tweets

# Download VADER lexicon (first time only)
nltk.download('vader_lexicon')

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Define languages and language codes
languages = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn"
}

# Search term
query = "Python"

# List to collect all results
results = []

# Loop through each language
for lang_name, lang_code in languages.items():
    print(f"\n{'='*30}\nLanguage: {lang_name}\n{'='*30}")

    try:
        tweets = get_recent_tweets(query, max_results=10, lang=lang_code)
    except Exception as e:
        print(f"❌ Error fetching tweets for {lang_name}: {e}")
        continue

    for i, tweet in enumerate(tweets, start=1):
        sentiment = sia.polarity_scores(tweet)
        compound = sentiment["compound"]

        # Classify sentiment
        if compound >= 0.05:
            label = "Positive"
        elif compound <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"

        print(f"\nTweet {i}: {tweet}")
        print(f"Sentiment: {sentiment} → {label}")

        # Save result to list
        results.append({
            "Language": lang_name,
            "Tweet": tweet,
            "Sentiment": label,
            "Compound Score": compound
        })

        time.sleep(1)

    # Avoid hitting Twitter API too fast
    print(f"\n✅ Finished {lang_name}. Waiting 60 seconds...")
    time.sleep(60)

# ✅ Save results to CSV
output_file = "sentiment_output.csv"

with open(output_file, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["Language", "Tweet", "Sentiment", "Compound Score"])
    writer.writeheader()
    writer.writerows(results)

print(f"\n✅ Sentiment results saved to {output_file}")
