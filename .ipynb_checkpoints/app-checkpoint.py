from flask import Flask, render_template, request, url_for, flash
# from flask import Flask, request, session, g, redirect, url_for, abort, \
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import json

app = Flask(__name__)

response = urlopen("https://raw.githubusercontent.com/hvo/datasets/master/nyc_restaurants_by_cuisine.json")
data = json.loads(response)

def getData(data,zip):
    res = []
    for d in data:
        if zip not in d['perZip']:
            res.append([d['cuisine'],0])
        else:
            res.append([d['cuisine'], d['perZip'][zip]])
    res.sort(key=lambda d:d[1],reverse=True)
    return res[:15]

@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'POST':
        zip = request.form['zipcode']
        flash(zip)

    return render_template('index.html')

if __name__ == '__main__':
   app.run(debug = True)
