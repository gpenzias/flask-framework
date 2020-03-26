from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import os
from matplotlib import pyplot as plt

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join('static','img_folder')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
  os.mkdir(app.config['UPLOAD_FOLDER'])

app.vars={}

@app.route('/index', methods=['GET','POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')
  else:
    # Request was a POST
    app.vars['name_stock_ticker'] = request.form['name_stock_ticker']

    print(f"Stock ticker name: {app.vars['name_stock_ticker']}")
    save_stock_ticker_graph_img(app.vars['name_stock_ticker'])

    return redirect('/graph')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/graph', methods=['GET'])
def graph():
  full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'graph.png')
  print(f"full_filename={full_filename}")
  return render_template("graph.html", user_image=full_filename)

  # return render_template('graph.html')

################################################################################################################
### Stock ticker code
################################################################################################################

# Get stock data
def save_stock_ticker_graph_img(name_stock_ticker):
  curr_ticker = name_stock_ticker
  curr_metric = 'close' #open, close, high, low

  params = {'ticker':curr_ticker,'api_key':'rKssTuYeBY6s29yRGzHA'}
  r = requests.get("https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json", params)

  col_names = [x['name'] for x in r.json()['datatable']['columns']]

  df = pd.DataFrame(r.json()['datatable']['data'],columns=col_names)

  fig = plt.figure(figsize=(12, 6))
  ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
  l1 = ax.plot(pd.to_datetime(df['date']), df[curr_metric])
  plt.xlabel('Date')
  plt.ylabel('Price (U.S. Dollars)')
  plt.title(f"Quandl WIKI Prices: {curr_ticker}: {curr_metric}")

  img_path = os.path.join('static','img_folder','graph.png')
  if os.path.exists(img_path):
    print('removing old img')
    os.remove(img_path)
  fig.savefig(img_path)

  print(f"Stock ticker name (2nd occurence): {app.vars['name_stock_ticker']}")


if __name__ == '__main__':
  app.run(port=33507)
