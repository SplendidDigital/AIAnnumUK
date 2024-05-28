# Stock Market Analyzer

#### Video Demo: [https://youtu.be/smnBsPz-90o?feature=shared]

#### Description:

This project is a web application that displays historical performance of prices of two stocks. It fetches stock price data from the Alpha Vantage API (free version), calculates annual growth and returns, and visualizes the results with a graph and table. However, this does not take into account adjustments like dividend and split. The data needed for adjustment we noticed are not available in Alpha Vantage free version of API.

Features:
Select stock exchange (NASDAQ, NYSE, AMEX)
Enter two stock symbols for comparison
Fetch historical stock data using the Alpha Vantage API
Display comparison results through graphs and tables

Fetching and Displaying Data: Upon user submission of stock symbols, the application initiates a process to fetch historical data from the Alpha Vantage API.
The fetched data includes daily stock prices and other relevant information for the specified symbols.
Utilizing the Pandas library, the application organizes the retrieved data into structured dataframes for efficient manipulation and analysis.
The historical data is then displayed on the user interface in graphical and tabular formats for easy interpretation.
Through this seamless process of data retrieval and presentation, users gain insights into the performance of their selected stocks over time.

Incorporating Adjustments: Due to limitations with free API access, adjustments related to dividends and stock splits have not been incorporated. These adjustments are crucial for a more accurate depiction of returns and should be considered for future development to make the application more practical for real-life usage.
Conclusion: With continuous development and innovation, this project aims to provide users with a comprehensive tool for making informed investment decisions in an ever-evolving market landscape, while acknowledging its current status as a learning demonstration rather than a fully practical application.

**Key Features:**

* **User-friendly interface:** Users can easily input two stock symbols.
* **Historical data analysis:**  Provides a clear comparison of stock growth over time.
* **Yearly return calculation:**  Shows annual percentage changes, giving insights into volatility and consistency.
* **Interactive chart:**  Allows users to visualize the growth trends.
* **Data table:**  Presents annual growth and returns in a structured format.

**Files:**

* `app.py`: Contains the main Flask application logic, routing, data fetching, and calculations.
* `index.html`: The main page with the stock symbol input form.
* `result.html`: The page that displays the comparison results (graph, table, etc.).

**Design Choices:**

* **Alpha Vantage API:** Chosen for its reliability and comprehensive historical data.
* **Flask:**  A lightweight and flexible web framework for building the application.
* **Chart.js:**  Used for creating the interactive graph.

**Potential Improvements:**

* **Does not take into account dividend adjustment, stock split:**  This feature could not be exploited as using free AlphaVantage API
* **More technical indicators:**  Could incorporate moving averages, RSI, etc.
* **Risk assessment:**  Add metrics to evaluate investment risk.
* **Portfolio simulation:**  Allow users to create hypothetical portfolios.


**How to Run:**

1. Install Flask and other required libraries:  `pip install Flask pandas matplotlib requests`
2. Set your Alpha Vantage API key in `app.py`.
3. Run the app:  `flask run`
4. Open a web browser and go to `http://127.0.0.1:5000/`
