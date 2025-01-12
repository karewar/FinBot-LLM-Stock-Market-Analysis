---
title: FinBot
emoji: 💬
colorFrom: yellow
colorTo: purple
sdk: gradio
sdk_version: 5.0.1
app_file: app.py
pinned: false
license: mit
short_description: To suggest stock behaviour from News/Technical Analysis
---

An example chatbot using [Gradio](https://gradio.app), [`huggingface_hub`](https://huggingface.co/docs/huggingface_hub/v0.22.2/en/index), and the [Hugging Face Inference API](https://huggingface.co/docs/api-inference/index).


README for Financial News and Technical Analysis Tool

Overview

The Financial News and Technical Analysis Tool is an interactive application built using Gradio, designed to assist users in analyzing stock performance. It provides financial news, sentiment analysis, technical data, and recommendations (Buy, Hold, or Sell) for selected companies based on AI-driven insights.

Key Features
- Financial News Fetching: Retrieves the latest news articles for a selected stock symbol using the NewsAPI.Sentiment Analysis: Analyzes the sentiment (Positive, Negative, Neutral) of news articles using TextBlob.
- Technical Analysis: Extracts and calculates key technical indicators such as RSI, MACD, and SMA using ta and yfinance.
- AI-Driven Recommendations: Generates stock recommendations using Groq's Llama 3 model.
- Interactive Interface: User-friendly Gradio interface with dropdowns and output fields.

Requirements: See the requirements.txt file

API Keys:
NewsAPI: Required for fetching news articles.
Groq: Required for accessing Groq’s AI model.

Installation

Clone the repository:

git clone <repository-url>
cd <repository-directory>

Install required Python packages:
pip install -r requirements.txt
Set environment variables for API keys:

export NEWSAPI_KEY=<your-newsapi-key>
export GROQ_API_KEY=<your-groq-api-key>

Usage
Launch the application:
python app.py
Open the Gradio interface in your browser.

Select a stock symbol from the dropdown and click Analyze.

- View financial news, sentiment analysis, technical data, and AI recommendations in the respective output sections.

Technical Indicators Explained:
RSI (Relative Strength Index): Indicates overbought or oversold conditions.
MACD (Moving Average Convergence Divergence): Highlights momentum direction.
SMA (Simple Moving Average): Tracks average closing prices over 50 and 200 days.

Application Flow:

Inputs --> Stock Symbol (Dropdown) --> Outputs --> Financial News --> Sentiment Analysis --> Technical Analysis --> Recommendation

Future Enhancements:
- Expand stock symbol support.
- Integrate advanced sentiment analysis models.
- Add more technical indicators and AI models.
- Enable real-time stock price tracking.

License
This project is licensed under the MIT License. See the LICENSE file for details.

