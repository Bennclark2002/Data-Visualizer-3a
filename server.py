from flask import Flask, render_template, request, url_for, flash, redirect, abort, send_file
import generate_graph
import os


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
    # Check if the chart file exists
    chart_exists = os.path.exists('static/chart.svg')
    return render_template('index.html', chart_exists=chart_exists)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)