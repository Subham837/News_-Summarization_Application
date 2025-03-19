import gradio as gr
import requests
import threading
from api import get_news, summarize_text
from analysis import analyze_sentiment, generate_sentiment_graph, generate_wordcloud
from utils import generate_tts
import plotly.express as px
import pandas as pd

def generate_sentiment_chart(sentiments):
    df = pd.DataFrame({"Sentiment": sentiments})  # Fixed column mismatch
    df["Count"] = 1  # Count occurrences
    df_grouped = df.groupby("Sentiment").count().reset_index()

    fig = px.pie(df_grouped, names="Sentiment", values="Count",
                 color="Sentiment",
                 color_discrete_map={"Positive": "#2ECC71", "Negative": "#E74C3C", "Neutral": "#3498DB"},
                 hole=0.4, title="Sentiment Analysis")
    return fig


# Optimized Processing Function
def process_news(company_name, query):
    if not company_name:
        return "❌ Please enter a company name.", None, None, None, None

    # Fetch news in a separate thread to reduce wait time
    articles = get_news(company_name, query)
    if not articles:
        return "❌ No news found!", None, None, None, None

    # Summarization and Sentiment Analysis (Parallel Processing)
    summaries, sentiments = [], []

    def summarize_and_analyze(article):
        summary = summarize_text(article["content"])  # Removed max_length to avoid errors
        sentiment = analyze_sentiment(summary)
        summaries.append(summary)
        sentiments.append(sentiment)

    threads = []
    for article in articles[:3]:
        thread = threading.Thread(target=summarize_and_analyze, args=(article,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    # Generate sentiment graph using Plotly
    sentiment_graph = generate_sentiment_chart(sentiments)

    # Generate word cloud
    wordcloud_path = generate_wordcloud(" ".join(summaries))

    # Generate Text-to-Speech
    tts_audio = generate_tts("\n".join(summaries[:2]))

    return summaries, sentiments, wordcloud_path, sentiment_graph, tts_audio

# Modern UI Design (Inspired by Your Image)
custom_css = """
body {
    background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
    font-family: 'Arial', sans-serif;
}
.gradio-container {
    max-width: 800px;
    margin: auto;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.2);
}
h1 {
    text-align: center;
    color: #fff;
    font-size: 28px;
}
input, button {
    border-radius: 10px !important;
    padding: 10px !important;
}
button {
    background: #ff7eb3 !important;
    color: white !important;
    font-size: 16px;
}
"""

# Gradio UI with Modern Design
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("<h1>📰 AI News Summarizer & Sentiment Analyzer</h1>")

    with gr.Row():
        company_input = gr.Textbox(label="Enter Company Name", placeholder="Tesla, Google, Microsoft...")
        query_input = gr.Textbox(label="Query (optional)", placeholder="Electric cars, AI, Stocks...")

    submit_button = gr.Button("🔍 Get News")

    with gr.Row():
        output_text = gr.Textbox(label="Summarized News", interactive=False)

    with gr.Row():
        sentiment_output = gr.Textbox(label="Sentiment Analysis", interactive=False)
        sentiment_graph = gr.Plot(label="Sentiment Analysis Graph")  # Using Plotly

    with gr.Row():
        wordcloud_output = gr.Image(label="Word Cloud")
        tts_audio = gr.Audio(label="🔊 Listen to Summary")

    submit_button.click(process_news, inputs=[company_input, query_input], 
                        outputs=[output_text, sentiment_output, wordcloud_output, sentiment_graph, tts_audio])

# Launch Gradio App
demo.launch(share=True)
