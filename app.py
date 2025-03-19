import gradio as gr
import requests
from api import get_news, summarize_text
from analysis import analyze_sentiment, generate_sentiment_graph, generate_wordcloud
from utils import generate_tts

def process_news(company_name, query):
    if not company_name:
        return "❌ Please enter a company name.", None, None, None, None

    # Fetch news articles
    articles = get_news(company_name, query)
    if not articles:
        return "❌ No news found!", None, None, None, None

    # Summarize and analyze sentiment
    summaries = [summarize_text(article["content"]) for article in articles[:3]]
    sentiments = [analyze_sentiment(summary) for summary in summaries]

    # Generate sentiment graph
    sentiment_graph_path = generate_sentiment_graph(sentiments)

    # Generate word cloud
    wordcloud_path = generate_wordcloud(" ".join(summaries))

    # Generate Text-to-Speech
    tts_audio = generate_tts("\n".join(summaries[:2]))

    return summaries, sentiments, wordcloud_path, sentiment_graph_path, tts_audio

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 📰 AI News Summarizer & Sentiment Analyzer")

    with gr.Row():
        company_input = gr.Textbox(label="Enter Company Name", placeholder="Tesla, Google, Microsoft...")
        query_input = gr.Textbox(label="Query (optional)", placeholder="Electric cars, AI, Stocks...")
    
    submit_button = gr.Button("🔍 Get News")

    with gr.Row():
        output_text = gr.Textbox(label="Summarized News", interactive=False)
    
    with gr.Row():
        sentiment_output = gr.Textbox(label="Sentiment Analysis", interactive=False)
        sentiment_graph = gr.Image(label="Sentiment Analysis Graph")

    with gr.Row():
        wordcloud_output = gr.Image(label="Word Cloud")
        tts_audio = gr.Audio(label="🔊 Listen to Summary")

    submit_button.click(process_news, inputs=[company_input, query_input], 
                        outputs=[output_text, sentiment_output, wordcloud_output, sentiment_graph, tts_audio])

# Launch Gradio app
demo.launch()
