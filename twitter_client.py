from dotenv import load_dotenv
import os
import tweepy

# Load environment variables from .env
load_dotenv()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Initialize Tweepy client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Function to fetch tweets in a specific language
def get_recent_tweets(query, max_results=10, lang="en"):
    # Ensure max_results is within Twitter API limits
    max_results = max(10, min(max_results, 100))
    
    # Add language filter to the query
    query_with_lang = f"{query} lang:{lang}"

    tweets = client.search_recent_tweets(
        query=query_with_lang,
        max_results=max_results,
        tweet_fields=["text"]
    )

    if tweets.data:
        return [tweet.text for tweet in tweets.data]
    return []
