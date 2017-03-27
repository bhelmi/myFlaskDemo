from flask import Flask, render_template, request, redirect
import quandl

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/graph', methods=['POST'])
def graph():

    ticker = request.form['ticker']
    processed_ticker = ticker.upper()
    return processed_ticker


def businessLogic(processed_ticker):
    
    quandl.ApiConfig.api_key = '8pUkznBCWKATjBv-NPZX'
    data = quandl.get_table('WIKI/PRICES')
    

if __name__ == '__main__':
  #app.run(port=33507)
  app.run(host='0.0.0.0')