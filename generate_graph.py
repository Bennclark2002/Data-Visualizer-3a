import requests
import pygal
from datetime import datetime, timedelta

def main(symbol,time_series,chart_type,start_date,end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")


    start_date_2 = start_date
    start_date = start_date.strftime("%Y-%m-%d")

# this is only used for intaday but dosent brake anything
    api_timeframe = start_date[:-3]


    r = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_{time_series}&symbol={symbol}&outputsize=full&month={api_timeframe}&interval=5min&apikey=V33ZAOO7VB64CV9C')
    all_data = r.json()
    data = Get_data_sorted(time_series,all_data)
    
    # switch statement since the json is diffrennt depending on time series

    Graph(symbol,time_series,chart_type,start_date,end_date,start_date_2,data)
def Get_data_sorted(time_series,all_data):
    if "Error Message" in all_data:
        return []
    match time_series:
        case "DAILY":
            return all_data["Time Series (Daily)"]
        case "INTRADAY":
            return all_data["Time Series (5min)"]
        case "WEEKLY":
            return all_data["Weekly Time Series"]
        case "MONTHLY":
            return all_data["Monthly Time Series"]
        case _:
            print("There has been an error with the program please close and try agian")


def Graph(symbol,time_series,chart_type,start_date,end_date,start_date_2,data):
    
    datetime_array = extract_x_axis(data,time_series,start_date,end_date)
  
    chart = pygal.Line(x_label_rotation=20)
    
    # magic god chatgpt taught me this
    datetime_array = sorted(list(set(datetime_array)))
    #make sure this runs after the lists are cleaned up
    graph_min, graph_max, open_array, high_array, low_array, close_array = extract_y_axis(time_series,data,datetime_array)

    # check which graph to use
    if chart_type == "Line":     
        chart = pygal.Line(x_label_rotation=20)
    elif chart_type == "Bar":
        chart = pygal.Bar(x_label_rotation=20)
    else:
         print("There has been an error with the program please close and try agian")

    #title
    formatted_end_date = end_date.strftime('%B %d, %Y')
    formatted_beginning_date = start_date_2.strftime('%B %d, %Y')
    chart.title = f'Stock data for {symbol}: {formatted_beginning_date} - {formatted_end_date}' 
    
    # x axis

    chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'),datetime_array)
    
    #y axis
    chart.add('Open', open_array) # adds a line each data is a data point on graph
    chart.add('High',  high_array)
    chart.add('Low',   low_array)
    chart.add('Close', close_array)

    #changing foramt to datetime

    
    chart.range = [graph_min,graph_max]
    chart.render_to_file('static/chart.svg') # finalizes the graph 

    return chart.render_response() # save this chart somewhere else


#this gets the datetime array which is the x axis in the graph
def extract_x_axis(data,time_series,start_date,end_date):
    new_datetime_array = []

    for key in data: 
        if time_series == "INTRADAY":
            date_object = datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
        else :
            date_object = datetime.strptime(key, "%Y-%m-%d")

        year = date_object.year
        month = date_object.month
        day =  date_object.day

        beginning_date_object = datetime.strptime(start_date, "%Y-%m-%d")
        # end_date_object = datetime.strptime(end_date, "%Y-%m-%d")
        if datetime(year,month,day) >= beginning_date_object and datetime(year,month,day) <= end_date:
            new_datetime_array.append(datetime(year,month,day))
    return new_datetime_array

def extract_y_axis(time_series,data,datetime_array):
    open_array = []
    high_array = []
    close_array = []
    low_array = []
    graph_min = float('inf')
    graph_max = -float('inf')
    # loop over datetime array to get the keys in order for the data object
    for key in datetime_array:
        if time_series == "INTRADAY":
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

    # fixes bug with the stock symbol being wrong
    if(graph_max == -float('inf') or graph_min == float('inf')):
        graph_min = 0
        graph_max = 0

    return  graph_min, graph_max, open_array, high_array, low_array, close_array 