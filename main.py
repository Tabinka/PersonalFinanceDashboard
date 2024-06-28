import pandas as pd
from dash import Dash, html


#df = pd.read_csv('financial_report.csv')    
app = Dash()

app.layout = [html.Div(children='Hello World')]

if __name__ == '__main__':
    app.run(debug=True)

