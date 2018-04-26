from flask import Flask, render_template, request, url_for, flash, jsonify
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
data = json.load(response)

def getData(data,zip):
    res = []
    for d in data:
        if zip not in d['perZip']:
            res.append([d['cuisine'],0])
        else:
            res.append([d['cuisine'], d['perZip'][zip]])
    res.sort(key=lambda d:d[1],reverse=True)
    return res[:15]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api',methods=['GET', 'POST'])
def api():
    error = ""
    try:
        zip = request.get_json(force=True)
        # print(type(zip),zip['name'])
        nowdata = getData(data,zip['name'])
        # print(nowdata)
        # nowdata = [['American', 1606], ['Cafe/Coffee/Tea', 402], ['Italian', 376], ['Japanese', 296], ['Chinese', 264], ['Pizza', 263], ['Thai', 197], ['Mexican', 174],
        # ['Asian', 161], ['French', 129], ['Middle Eastern', 129], ['Sandwiches', 113], ['Hamburgers', 98], ['Pizza/Italian', 88], ['Spanish', 82]]
        return jsonify(nowdata)
    except:
        # print("error")
        return error


if __name__ == '__main__':
   app.run(debug = True)
