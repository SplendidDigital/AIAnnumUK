from flask import Flask, render_template, request
import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO, StringIO
import base64
import csv
import datetime

app = Flask(__name__)

# Replace with your actual API key from Alpha Vantage
API_KEY = "FI5B9EM5VOZTW6WJ"

def fetch_stock_symbols(exchange):
    url = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={API_KEY}&exchange={exchange}"
    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.headers['Content-Type'] == 'application/x-download':
            csv_data = StringIO(response.text)
            csv_reader = csv.DictReader(csv_data)
            return [row['symbol'] for row in csv_reader if not row['symbol'].isdigit()]
        else:
            print("Unexpected response content type:", response.headers['Content-Type'])
            return []

    except requests.RequestException as e:
        print(f"Error fetching symbols: {e}")
        return []

def fetch_historical_data(symbol):
    ten_years_ago = datetime.datetime.now() - datetime.timedelta(days=10*365)
    start_date = ten_years_ago.strftime('%Y-%m-%d')

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if "Time Series (Daily)" in data:
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
            df = df.rename(columns={"4. close": "close"})
            df["close"] = pd.to_numeric(df["close"])
            df.index = pd.to_datetime(df.index)
            df = df[df.index >= start_date]
            df.sort_index(inplace=True)
            return df

        return None

    except requests.RequestException as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_growth(df, start_value=100):
    df = df.resample("Y").last()
    growth = (df["close"] / df["close"].iloc[0]) * start_value
    yearly_returns = (growth.pct_change() * 100).round(2)
    return growth, yearly_returns

def compare_stocks(symbol1, symbol2):
    df1 = fetch_historical_data(symbol1)
    df2 = fetch_historical_data(symbol2)

    if df1 is None or df2 is None:
        return None, None, None, None, None, None, f"Could not fetch data for one or both symbols."

    common_start_date = max(df1.index.min(), df2.index.min())

    df1 = df1[df1.index >= common_start_date]
    df2 = df2[df2.index >= common_start_date]

    if df1.empty or df2.empty:
        return None, None, None, None, None, None, "No overlapping data available for the selected stocks."
    else:
        growth1, yearly_returns1 = calculate_growth(df1.copy())
        growth2, yearly_returns2 = calculate_growth(df2.copy())

        cumulative_returns1 = [0]
        cumulative_returns2 = [0]
        for val1, val2 in zip(growth1.values[1:], growth2.values[1:]):
            cumulative_returns1.append(((val1 - growth1.values[0]) / 100) * 100)
            cumulative_returns2.append(((val2 - growth2.values[0]) / 100) * 100)

        return growth1, growth2, yearly_returns1, yearly_returns2, cumulative_returns1, cumulative_returns2, None

@app.route("/", methods=["GET", "POST"])
def index():
    symbols = []
    if request.method == "POST":
        exchange = request.form["exchange"]
        symbol1 = request.form["symbol1"]
        symbol2 = request.form["symbol2"]
        symbols = fetch_stock_symbols(exchange)

        growth1, growth2, yearly_returns1, yearly_returns2, cumulative_returns1, cumulative_returns2, error_message = compare_stocks(symbol1, symbol2)

        if error_message:
            return render_template("index.html", symbols=symbols, error_message=error_message)

        plt.figure(figsize=(10, 6))
        plt.plot(growth1.index, growth1.values, label=symbol1)
        plt.plot(growth2.index, growth2.values, label=symbol2)
        plt.xlabel("Year")
        plt.ylabel("Value of $100 Investment")
        plt.title("Stock Comparison")
        plt.legend()

        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

        start_date = growth1.index[0].strftime('%Y-%m-%d')
        end_date = growth1.index[-1].strftime('%Y-%m-%d')
        final_value1 = growth1.values[-1]
        final_value2 = growth2.values[-1]

        comparison_message = (
            f"On {start_date}, $100 invested in {symbol1} would be worth ${final_value1:.2f} on {end_date}.\n"
            f"On {start_date}, $100 invested in {symbol2} would be worth ${final_value2:.2f} on {end_date}."
        )

        table_data = []
        for year, val1, ret1, val2, ret2, cum_ret1, cum_ret2 in zip(
            growth1.index.year,
            growth1.values,
            yearly_returns1.values,
            growth2.values,
            yearly_returns2.values,
            cumulative_returns1,
            cumulative_returns2
        ):
            table_data.append({
                "year": year,
                "val1": val1,
                "ret1": ret1,
                "val2": val2,
                "ret2": ret2,
                "cum_ret1": cum_ret1,
                "cum_ret2": cum_ret2
            })

        return render_template(
            "result.html",
            img_data=img_base64,
            comparison_message=comparison_message,
            table_data=table_data,
            start_date=start_date,
            end_date=end_date,
            symbol1=symbol1,
            symbol2=symbol2,
        )
    else:
        # Default to NASDAQ symbols on initial load
        symbols = fetch_stock_symbols('NASDAQ')
    return render_template("index.html", symbols=symbols)

if __name__ == "__main__":
    app.run(debug=True)
