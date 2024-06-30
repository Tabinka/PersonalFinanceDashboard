import pandas as pd
from dash import Dash
from basic_layout import BasicLayout
from starting_layout import StartingLayout

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(external_stylesheets=external_stylesheets)

## when file uploaded, it will show graphs (try, except here is not nessesery)
try:
    df = pd.read_csv('data_test.csv')
    page = BasicLayout(df, app)
except:
    start = StartingLayout(app)

if __name__ == '__main__':
    app.run(debug=True)
