import os
import logging
from datetime import datetime, timedelta
from newsapi.newsapi_client import NewsApiClient
from textblob import TextBlob
import yfinance as yf
import pandas as pd
import ta
import gradio as gr
from groq import Groq

# Set up logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve API keys from environment variables
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

# Use Groq's Llama 3 model for decision making
MODEL = "llama3-70b-8192"

# Define the list of companies and their stock symbols
top_companies = [
    {"name": "Tesla", "symbol": "TSLA"},
    {"name": "Meta (Facebook)", "symbol": "META"},
    {"name": "Visa", "symbol": "V"},
    {"name": "Procter & Gamble", "symbol": "PG"},
    {"name": "Coca-Cola", "symbol": "KO"},
    {"name": "NVIDIA", "symbol": "NVDA"},
    {"name": "Johnson & Johnson", "symbol": "JNJ"},
    {"name": "Exxon Mobil", "symbol": "XOM"},
    {"name": "Apple", "symbol": "AAPL"},
    {"name": "Microsoft", "symbol": "MSFT"},
    {"name": "Amazon", "symbol": "AMZN"},
    {"name": "Google (Alphabet)", "symbol": "GOOGL"},
    
]

# Fetch financial news with sentiment analysis
def fetch_financial_news_with_sentiment(stock_symbol=None, page_size=5, days=1):
    try:
        newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
        query = stock_symbol if stock_symbol else "financial news"
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        articles = newsapi.get_everything(
            q=query,
            language='en',
            from_param=start_date.strftime('%Y-%m-%d'),
            to=end_date.strftime('%Y-%m-%d'),
            sort_by='publishedAt',
            page_size=page_size
        )

        news_results = []
        sentiment_results = []

        for article in articles.get('articles', []):
            title = article.get('title', '[Title Unavailable]')
            description = article.get('description', '[Description Unavailable]')
            url = article.get('url', 'URL Unavailable')
            sentiment = analyze_sentiment(title) if title else "Neutral"

            news_results.append(f"Title: {title}\nDescription: {description}\nURL: {url}")
            sentiment_results.append(f"Sentiment: {sentiment}")

        return "\n\n".join(news_results), "\n\n".join(sentiment_results)
    except Exception as e:
        return f"Error fetching news: {e}", ""

# Perform sentiment analysis
def analyze_sentiment(text):
    try:
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        if polarity > 0.1:
            return "Positive"
        elif polarity < -0.1:
            return "Negative"
        else:
            return "Neutral"
    except Exception as e:
        return f"Error analyzing sentiment: {e}"

# Fetch technical data
def fetch_technical_data(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        data = stock.history(period="1y")

        if data.empty:
            return "No data found for this stock symbol."

        data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()
        macd = ta.trend.MACD(data['Close'])
        data['MACD'] = macd.macd()
        data['MACD_Signal'] = macd.macd_signal()
        data['SMA_50'] = data['Close'].rolling(window=50).mean()
        data['SMA_200'] = data['Close'].rolling(window=200).mean()

        latest_technical_data = {
            "RSI": data['RSI'].iloc[-1],
            "MACD": data['MACD'].iloc[-1],
            "MACD Signal": data['MACD_Signal'].iloc[-1],
            "50 Day SMA": data['SMA_50'].iloc[-1],
            "200 Day SMA": data['SMA_200'].iloc[-1],
        }

        return pd.Series(latest_technical_data).to_string()
    except Exception as e:
        return f"Error fetching technical data: {e}"

# Generate buy/hold/sell recommendation using Groq
def generate_recommendation(news, technical_data):
    prompt = f"Based on the following news:\n{news}\nAnd the technical indicators:\n{technical_data}\nWhat would you recommend: Buy, Hold, or Sell? Provide a brief explanation."
    
    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a financial analyst providing stock recommendations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    
    return response.choices[0].message.content.strip()

# Define Gradio interface
def analyze_stock(stock_symbol):
    symbol = stock_symbol.split('(')[-1].split(')')[0]
    news, sentiment = fetch_financial_news_with_sentiment(symbol, days=1)
    technical_data = fetch_technical_data(symbol)
    recommendation = generate_recommendation(news, technical_data)
    return news, sentiment, technical_data, recommendation

with gr.Blocks() as demo:
    gr.Markdown("## Financial News and Technical Analysis Tool")

    with gr.Row():
        stock_input = gr.Dropdown(
            choices=[f"{company['name']} ({company['symbol']})" for company in top_companies],
            label="Enter Stock Symbol (currently supports only a few companies)",
            info="Select a company from the dropdown"
        )
        analyze_button = gr.Button("Analyze")

    recommendation_output = gr.Textbox(label="Recommendation", interactive=False)
    
    with gr.Row():
        news_output = gr.Textbox(label="Financial News", interactive=False, lines=10)
        sentiment_output = gr.Textbox(label="Sentiment Analysis", interactive=False, lines=10)
    technical_output = gr.Textbox(label="Technical Analysis", interactive=False)

    analyze_button.click(
        analyze_stock,
        inputs=[stock_input],
        outputs=[news_output, sentiment_output, technical_output, recommendation_output]
    )

if __name__ == "__main__":
    demo.launch()

