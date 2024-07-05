import pandas as pd
from dash import Dash
from basic_layout import BasicLayout
from starting_layout import StartingLayout

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

if __name__ == '__main__':
    app = Dash(__name__, external_stylesheets=external_stylesheets)
    
    df = pd.read_csv('bank_transactions_06_2024.csv')
    layout = BasicLayout(df, app)
    
    app.run(debug=True)
