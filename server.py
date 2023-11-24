from flask import Flask, render_template, request, url_for, flash, redirect, abort, send_file
from datetime import datetime
import generate_graph
import os
import csv




# This is bad code and only allows one person to use the server at a time, the reqs dosent say to fix this will work later
if os.path.exists('static/chart.svg'):
    os.remove('static/chart.svg')

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/submit', methods=['POST'])
def submit():
    # Access form data using request.form
    symbol = request.form['symbol']
    time_series = request.form['timeSeries']
    chart_type = request.form['chartType']
    start_date = request.form['startDate']
    end_date = request.form['endDate']
    
    generate_graph.main(symbol,time_series,chart_type,start_date,end_date)

    return redirect(url_for('home'))



#landing page where they are initilly given the choices for their graph
@app.route('/')
def home():
    # Read the csv file then get the row of stock symbols
    with open('stocks.csv', 'r')as file:
        symbols = [row['Symbol'] for row in csv.DictReader(file)]

    # Check if the chart file exists
    chart_exists = os.path.exists('static/chart.svg')
    
    # this is the date used to limit the html input value
    now = datetime.now().strftime('%Y-%m-%d')

    # no idea why but setting it to be itself fixed an issue
    return render_template('index.html', symbols=symbols ,chart_exists=chart_exists, now=now)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)