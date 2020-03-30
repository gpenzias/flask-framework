from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import os
# from matplotlib import pyplot as plt

import jinja2
from bokeh.embed import components
from bokeh.plotting import figure

app = Flask(__name__)


app.vars={}

@app.route('/index', methods=['GET','POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')
  else:
    # Request was a POST
    app.vars['name_stock_ticker'] = request.form['name_stock_ticker']

    return redirect('/graph')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/graph', methods=['GET'])
def graph():
  print(f"Stock ticker name: {app.vars['name_stock_ticker']}")
  template, script, div = create_stock_ticker_graph(app.vars['name_stock_ticker'])
  return template.render(script=script, div=div)

################################################################################################################
### Stock ticker code
################################################################################################################

def load_stock_data_to_dataframe(name_stock_ticker):
  name_stock_ticker = name_stock_ticker

  params = {'ticker': name_stock_ticker, 'api_key': 'rKssTuYeBY6s29yRGzHA'}
  r = requests.get("https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json", params)

  col_names = [x['name'] for x in r.json()['datatable']['columns']]

  df = pd.DataFrame(r.json()['datatable']['data'], columns=col_names)
  return df

# Get stock data
def create_stock_ticker_graph(name_stock_ticker):
  curr_metric = 'close' #could change to open, high, low, etc.

  df = load_stock_data_to_dataframe(name_stock_ticker)

  # IMPORTANT NOTE!! The version of BokehJS loaded in the template should match
  # the version of Bokeh installed locally.

#   < link
#   href = "http://cdn.pydata.org/bokeh/release/bokeh-0.13.0.min.css"
#   rel = "stylesheet"
#   type = "text/css"
# >

  template = jinja2.Template("""
  <!DOCTYPE html>
  <html lang="en-US">
  
  
  
  <script 
      src="http://cdn.pydata.org/bokeh/release/bokeh-2.0.1.min.js"
  ></script>
  
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta name="description" content="Flask app for 12-day course TDI.">
        <meta name="author" content="gpenzias">

        <title>Graph of stock price Data</title>

            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

        <style>
        body {
          padding-top: 70px;
        }
        </style>


    </head>

	<body>
        <!-- navigation -->
        <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
          <div class="container">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#nav-1">
              <span class="sr-only">Toggle navigation</span>
              </button>
              <span class="navbar-brand">Ticker Lookup App</span>
            </div>
        
            <div class="collapse navbar-collapse" id="nav-1">
              <ul class="nav navbar-nav">
                <li class="nav-item">
                  <a class="nav-link" href="/index">Home</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="https://github.com/gpenzias/flask-framework">GitHub</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="https://www.thedataincubator.com/12day.html">12-day</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>



      <h1>Hello TDI!</h1>

      <p> Please enjoy this simple plot of stock closing prices </p>

      {{ script }}

      {{ div }}

  </body>

  </html>
  """)

  # create a new plot (with a title) using figure
  p = figure(x_axis_type="datetime", plot_width=400, plot_height=400,
             title=f"Quandl WIKI Prices: {name_stock_ticker}: {curr_metric}")

  # add a line renderer
  p.line(pd.to_datetime(df['date']), df[curr_metric], line_width=1)
  p.xaxis.axis_label = 'Date'
  p.yaxis.axis_label = 'Price (U.S. Dollars)'

  # Get html components of plot
  script, div = components(p)

  return template, script, div
  """
  # Old plot generation code with matplotlib, before bokeh 2.0.1 was released. 
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
  """

  print(f"Stock ticker name (2nd occurence): {app.vars['name_stock_ticker']}")


if __name__ == '__main__':
  app.run(port=33507)
