import pandas as pd
from dash import dcc, html, dash_table
import plotly.express as px


class BasicLayout:
      def __init__(self, data, app):
            self.data = data
            self.app = app
            self.app.layout = self.start_page()

      def start_page(self):
            df = self.data
            df['Date'] = pd.to_datetime(df['Date'])
            df['Month'] = df['Date'].dt.to_period('M').astype(str)
            
            income = df[df['Amount'] > 0].groupby('Month')['Amount'].sum()
            expenses = df[df['Amount'] < 0].groupby('Month')['Amount'].sum()
            income_expense = pd.DataFrame({'Income': income, 'Expenses': expenses}).reset_index()
            
            income_expense_chart = px.bar(
                  income_expense,
                  x='Month',
                  y=['Income', 'Expenses'],
                  barmode='group',
                  title='Total Income vs. Total Expenses'
                  )
            
            return html.Div([
                  html.H5("Render saved file"),
                  dash_table.DataTable(
                  self.data.to_dict('records'),
                  [{'name': i, 'id': i} for i in self.data.columns]
                  ),
                  html.Hr(),
                  dcc.Graph(id='income-expense-chart', figure=income_expense_chart)])