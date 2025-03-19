import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from transformers import pipeline

# ✅ Load Sentiment Analysis Model
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    """Analyzes sentiment and returns sentiment label with confidence."""
    result = sentiment_analyzer(text)[0]
    return result['label'], result['score']

def generate_sentiment_graph(sentiments):
    """Creates a bar chart for sentiment analysis results."""

    assets_dir = "assets"

    # ✅ Ensure 'assets/' is a folder
    if os.path.exists(assets_dir) and not os.path.isdir(assets_dir):
        os.remove(assets_dir)  # Delete if it's a file
        os.makedirs(assets_dir)  # Recreate as a folder
    elif not os.path.exists(assets_dir):
        os.makedirs(assets_dir)

    # ✅ Extract sentiment data
    labels = [s[0] for s in sentiments]  
    scores = [s[1] for s in sentiments]  

    # ✅ Create bar chart
    plt.figure(figsize=(6, 3))
    plt.bar(labels, scores, color=["green" if lbl == "POSITIVE" else "red" for lbl in labels])
    plt.xlabel("Sentiment")
    plt.ylabel("Confidence Score")
    plt.title("Sentiment Analysis Results")

    # ✅ Save the graph inside 'assets/' folder
    graph_path = os.path.join(assets_dir, "sentiment_graph.png")
    plt.savefig(graph_path)
    plt.close()

    return graph_path

def generate_wordcloud(text):
    """Generates a word cloud and ensures 'assets/' is always a folder."""

    assets_dir = "assets"

    # ✅ Ensure 'assets/' is a folder
    if os.path.exists(assets_dir) and not os.path.isdir(assets_dir):
        os.remove(assets_dir)  # Delete if it's a file
        os.makedirs(assets_dir)  # Recreate as a folder
    elif not os.path.exists(assets_dir):
        os.makedirs(assets_dir)

    # ✅ Generate and save Word Cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    wordcloud_path = os.path.join(assets_dir, "wordcloud.png")
    wordcloud.to_file(wordcloud_path)

    return wordcloud_path
