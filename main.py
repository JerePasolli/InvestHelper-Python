import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "7A6QM5TSK41G1RXY"
NEWS_API_KEY = "3e8ef73b69b047d6850373e37cbe25eb"
TWILIO_SID = "ACe6ae3d7f2ed1e86e740dc869282fb377"
TWILIO_TOKEN = "b09c2d54aa7dec508df775f754ac3b0f"

stock_params = {
    "apikey": STOCK_API_KEY,
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]  # allows to access items by index
yesterday_closing_price = float(stock_data_list[0]["4. close"])
day_before_yesterday_closing_price = float(stock_data_list[1]["4. close"])

difference = yesterday_closing_price - day_before_yesterday_closing_price
up_down = None
if difference > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"

diff_percent = round((difference / yesterday_closing_price) * 100)

if abs(diff_percent) >= 2:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    three_articles = news_data[:3]  # the first three news only
    ready_articles = [(f"{STOCK}: {up_down}{diff_percent}%\n\n"
                       f"Headline: {article['title']}."
                       f"\n\nBrief: {article['description']}") for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_TOKEN)
    for article in ready_articles:
        message = client.messages.create(body=article,
                                         from_="+18582408590",
                                         to="your_number_here")
