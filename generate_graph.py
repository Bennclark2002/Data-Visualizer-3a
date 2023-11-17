import requests
import redis
import pygal
from flask import Flask
from datetime import datetime, timedelta


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

# api_symbol = userInput.get_stock_symbol()
# graph_type = userInput.get_chart_type()
# api_timeSeries = userInput.get_time_series()
# beginning_date = userInput.get_start_date()
# end_date = userInput.get_end_date(beginning_date)

# this is test development
api_symbol = "IBM"
api_timeSeries = "1"
graph_type = "2"
beginning_date = datetime.strptime("2000-01-01", "%Y-%m-%d")
end_date = datetime.strptime("2000-01-29", "%Y-%m-%d")


beginning_date_2 = beginning_date

beginning_date = beginning_date.strftime("%Y-%m-%d")

match api_timeSeries:
    case "1":
        api_timeSeries = "INTRADAY"
    case "2":
        api_timeSeries = "DAILY"
    case "3":
        api_timeSeries = "WEEKLY"
    case "4":
        api_timeSeries = "MONTHLY"

match graph_type:
    case "1":
        graph_type = "Bar"
    case "2":
        graph_type = "Line"

# this is only used for intaday but dosent brake anything
api_timeframe = beginning_date[:-3]
graph_min = float('inf')
graph_max = -float('inf')

# these arrays will be used to populate the y axis
open_array = []
high_array = []
low_array = []
close_array = []

# extract_x_axis will populate and convert to array once the loop for data runs
datetime_array = []

r = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_{api_timeSeries}&symbol={api_symbol}&outputsize=full&month={api_timeframe}&interval=5min&apikey=V33ZAOO7VB64CV9C')
all_data = r.json()

# switch statement since the json is diffrennt depending on time series
match api_timeSeries:
    case "DAILY":
        data = all_data["Time Series (Daily)"]
    case "INTRADAY":
        data = all_data["Time Series (5min)"]
    case "WEEKLY":
        data = all_data["Weekly Time Series"]
    case "MONTHLY":
        data = all_data["Monthly Time Series"]
    case _:
        print("There has been an error with the program please close and try agian")

def Graph():
    global datetime_array, open_array, high_array, low_array, close_array  # Declare variables as global
    datetime_array = []
    open_array = []
    high_array = []
    low_array = []
    close_array = []

    extract_x_axis()
    
    # magic god chatgpt taught me this
    datetime_array = sorted(list(set(datetime_array)))
    #make sure this runs after the lists are cleaned up
    extract_y_axis()

    # check which graph to use
    if graph_type == "Line":     
        chart = pygal.Line(x_label_rotation=20)
    elif graph_type == "Bar":
        chart = pygal.Bar(x_label_rotation=20)
    else:
         print("There has been an error with the program please close and try agian")

    #title
    formatted_end_date = end_date.strftime('%B %d, %Y')
    formatted_beginning_date = beginning_date_2.strftime('%B %d, %Y')
    chart.title = f'Stock data for {api_symbol}: {formatted_beginning_date} - {formatted_end_date}' 
    
    # x axis

    chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'),datetime_array)
    
    #y axis
    chart.add('Open', open_array) # adds a line each data is a data point on graph
    chart.add('High',  high_array)
    chart.add('Low',   low_array)
    chart.add('Close', close_array)

    #changing foramt to datetime

    
    chart.range = [graph_min,graph_max]
    chart.render() # finalizes the graph 

    return chart.render_response() # save this chart somewhere else


#this gets the datetime array which is the x axis in the graph
def extract_x_axis():
    global datetime_array  # Declare datetime_array as a global variable
    global beginning_date
    global end_date

    for key in data: 
        if api_timeSeries == "INTRADAY":
            date_object = datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
        else :
            date_object = datetime.strptime(key, "%Y-%m-%d")
        year = date_object.year
        month = date_object.month
        day =  date_object.day

        beginning_date_object = datetime.strptime(beginning_date, "%Y-%m-%d")
        # end_date_object = datetime.strptime(end_date, "%Y-%m-%d")
        if datetime(year,month,day) >= beginning_date_object and datetime(year,month,day) <= end_date:
            datetime_array.append(datetime(year,month,day))  

def extract_y_axis():
    global graph_max
    global graph_min
    # loop over datetime array to get the keys in order for the data object
    for key in datetime_array:
        if api_timeSeries == "INTRADAY":
            # Add 11 hours to the key
            date_object = key + timedelta(hours=11)
            # Convert the datetime object back to a string
            newKey = date_object.strftime("%Y-%m-%d %H:%M:%S")
        else :
            newKey = key.strftime("%Y-%m-%d")
        # adds all the data to the relevant places and turns it into float for the graph
        open_array.append(float(data[newKey]["1. open"]))
        high_array.append(float(data[newKey]["2. high"]))
        low_array.append(float(data[newKey]["3. low"]))
        close_array.append(float(data[newKey]["4. close"]))

        if graph_max < float(data[newKey]["2. high"]):
            graph_max = float(data[newKey]["2. high"])
        if graph_min > float(data[newKey]["3. low"]):
            graph_min = float(data[newKey]["3. low"])
        
    # ideally you would want to have this file sepreate from the main function and have this be a "server" program.... but the project is to small to warrent it
    # so instead we have the two files meshed together.

def main():
    return Graph()


