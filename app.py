from flask import Flask, render_template, request, redirect
import quandl
import quandl
import requests
import simplejson as json
import pandas as pd
import urllib
from bokeh.plotting import figure
from bokeh.io import output_notebook, output_file, show
from bokeh.models import DatetimeTickFormatter
from bokeh.embed import components
from bokeh.util.string import encode_utf8


app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')
  else:
        #request was a post
        app.vars['ticker'] = request.form['ticker']
        app.vars['checklists'] = request.form.getlist('features')
        print app.vars['ticker']
        print app.vars['checklists']
        return redirect('graph')
        
@app.route('/graph')
def graph():
        quandl.ApiConfig.api_key = '8pUkznBCWKATjBv-NPZX'
        serviceURL = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?'
        
        url = serviceURL + 'ticker=' + app.vars['ticker'] + '&api_key=' + quandl.ApiConfig.api_key
        print url
        r = requests.get(url)
        print r.status_code
        
        data_json = r.json()
        data_df = pd.DataFrame.from_records(data_json['datatable']["data"], columns = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume', 'ex-dividened', 'split_ratio', 'adj_open', 'adj_high', 'adj_low', 'adj_close', 'adj_volume'])
        
        print data_df.shape
        
        data_df_date = pd.to_datetime(data_df['date'])
        
        print data_df_date.head()
        
        colors_list = ['blue', 'brown', 'red', 'green']
        p = figure (title="Data from Quandle Wiki/Price", x_axis_label = 'price', y_axis_label = 'date')

        for idx, val in enumerate(app.vars['checklists']):
            p.line(data_df_date, data_df[val], legend=val, line_width = 2, color=colors_list[idx])
            print(data_df[val].head())
        #p = figure()
        #p.circle([1,2], [3,4])
        
        script, div = components(p)
        print script
        print div
        
        #html = render_template('embed.html',plot_script=script, plot_div=div, plot_resources=plot_resources)
        #return encode_utf8(html)
        html = render_template('graph.html', div = div, script = script)
        return encode_utf8(html)

#    return render_template('graph.html')

#    ticker = request.form['ticker']
#    processed_ticker = ticker.upper()
#    return processed_ticker


#def businessLogic(processed_ticker):
    
#    quandl.ApiConfig.api_key = '8pUkznBCWKATjBv-NPZX'
#    data = quandl.get_table('WIKI/PRICES')
    

if __name__ == '__main__':
  #app.run(port=33507)
  app.run(host='0.0.0.0')