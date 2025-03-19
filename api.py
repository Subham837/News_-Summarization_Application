import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import nltk
import concurrent.futures  # ✅ Enables parallel processing

nltk.download("punkt")

# ✅ Load a Faster Summarization Model (DistilBART for Speed)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")  # ✅ 3X Faster Model

# ✅ NewsAPI Configuration
NEWS_API_KEY = "c272443116c025bc14b1e6bb62d7a1d8" 
NEWS_API_URL = "https://gnews.io/api/v4/search"

# ✅ Function to Scrape Full Article (Limits Text for Speed)
def scrape_full_article(url):
    """Scrapes only the first 3 paragraphs of an article to reduce processing time."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # ✅ Fetch only first 3 paragraphs (Reduces processing time)
            paragraphs = soup.find_all("p")[:3]  
            full_text = " ".join([para.get_text() for para in paragraphs])

            return full_text if len(full_text) > 50 else "Full article unavailable."
        else:
            return "Could not retrieve article."
    except Exception as e:
        return f"Error fetching article: {str(e)}"

# ✅ Function to Summarize Text (Dynamically Adjusts Length)
def summarize_text(text):
    """Summarizes text efficiently with adaptive length settings."""
    
    if not text.strip():  # ✅ Check if text is empty
        return "No content available to summarize."

    max_input_length = 400  # ✅ Reduce input size for speed
    words = text.split()

    # ✅ Truncate text to 400 words for faster summarization
    if len(words) > max_input_length:
        text = " ".join(words[:max_input_length])  

    # ✅ Dynamically adjust summarization length
    input_length = len(text.split())
    max_summary_length = max(50, int(input_length * 0.5))  # 50% of input
    min_summary_length = max(25, int(input_length * 0.2))  # 20% of input

    return summarizer(text, max_length=max_summary_length, min_length=min_summary_length, do_sample=False)[0]["summary_text"]

# ✅ Function to Fetch News (Parallel Processing for Speed)
def get_news(company, query=None):
    """Fetches news articles from GNews API and scrapes full content in parallel."""
    params = {
        "q": f"{company} {query}" if query else company,
        "token": NEWS_API_KEY,  
        "lang": "en",
        "sortby": "publishedAt",
        "max": 5  # ✅ Limit to 5 results for faster performance
    }
    
    response = requests.get(NEWS_API_URL, params=params)

    if response.status_code == 200:
        articles = response.json().get("articles", [])

        results = []

        # ✅ Process news articles in parallel (Boosts Speed)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:  # ✅ Use 5 threads
            future_to_article = {executor.submit(scrape_full_article, art["url"]): art for art in articles}
            for future in concurrent.futures.as_completed(future_to_article):
                art = future_to_article[future]
                try:
                    full_text = future.result()  # ✅ Get scraped text
                    
                    # ✅ Ensure non-empty content before summarization
                    summarized_text = summarize_text(full_text) if full_text and full_text != "Full article unavailable." else "Summary unavailable."

                    results.append({
                        "title": art["title"],
                        "content": summarized_text,
                        "url": art["url"],
                        "image": art.get("image", ""),
                        "publishedAt": art["publishedAt"],
                        "source": art["source"]["name"]
                    })
                except Exception as e:
                    print(f"Error processing article: {str(e)}")

        return results
    
    return []
