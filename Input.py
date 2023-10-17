import requests
import pygal 
from lxml import html

stock_symbol = input("Enter the symbol for the company: ")
chart_type = input("Enter the chart type (line/bar): ").lower()
time_series_func = input("Enter the time series function (1d/1m/1y):").lower()
start_date = input("Enter the beginning date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD)")

