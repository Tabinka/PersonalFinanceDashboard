import pandas as pd
from dash import Dash, html
from basic_layout import basic_layout
from starting_layout import starting_layout

app = Dash()
start = starting_layout(app) ## start with upload button

## when file uploaded, it will show graphs (try, except here is not nessesery)
try:
    df = pd.read_csv('financial_report.csv')
    page = basic_layout(df, app)
except:
    start.render()

if __name__ == '__main__':
    app.run(debug=True)
