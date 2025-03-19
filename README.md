# News_-Summarization_Application

title: AI News Summarizer & Sentiment Analyzer
emoji: 🚀
colorFrom: blue
colorTo: red
sdk: gradio
sdk_version: 5.22.0
app_file: app.py
pinned: false

The News Summarization & Sentiment Analyzer is an AI-powered application designed to scrape news articles, summarize them using NLP techniques, analyze sentiment, and convert text to speech for better accessibility. The project is deployed on Hugging Face Spaces.

Features

Web Scraping: Uses BeautifulSoup to extract news articles from online sources.

Summarization: Implements transformer-based models for text summarization.

Sentiment Analysis: Determines the sentiment (positive, neutral, or negative) of the summarized news.

Text-to-Speech (TTS): Converts summarized news into speech for better accessibility.

Query System: Allows users to search and filter news summaries based on keywords.

Attractive UI: A user-friendly interface for enhanced experience.

Industrial-Level Deployment: Hosted on Hugging Face Spaces for real-world accessibility.

Tech Stack

Frontend: Streamlit (for UI)

Backend: Python, Flask

Web Scraping: BeautifulSoup

NLP Models: Hugging Face Transformers (BART/T5 for summarization, BERT for sentiment analysis)

Text-to-Speech: gTTS or Hugging Face TTS models

Deployment: Hugging Face Spaces
