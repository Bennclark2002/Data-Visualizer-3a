from flask import Flask, render_template, request, url_for, flash, redirect, abort, send_file
import generate_graph

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'




# build out a graph when the form is submited
@app.route('/chart.svg')
def get_chart():
    return generate_graph.main()
#landing page where they are initilly given the choices for their graph
@app.route('/')
def home():
    return render_template("index.html")
    

app.run(host="0.0.0.0", port=5001)