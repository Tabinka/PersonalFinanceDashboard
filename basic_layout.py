import pandas as pd
from dash import dcc, html, dash_table
import plotly.express as px


class BasicLayout:
      def __init__(self, data, app):
            self.data = data
            self.app = app
            self.app.layout = self.start_page()

      def start_page(self):
            income_expense_chart, df_income_expense = self.income_expense(self.data)
            savings_chart = self.savings(df_income_expense)
            
            return html.Div([
                  html.H5("Render saved file"),
                  dash_table.DataTable(
                  self.data.to_dict('records'),
                  [{'name': i, 'id': i} for i in self.data.columns]
                  ),
                  html.Hr(),
                  dcc.Graph(id='income-expense-chart', figure=income_expense_chart),
                  dcc.Graph(id='monthly-savings-chart', figure=savings_chart)])
            
      def income_expense(self, df):
            df['Date'] = pd.to_datetime(df['Date'])
            df['Month'] = df['Date'].dt.to_period('M').astype(str)
            
            income_expense = df.groupby('Month').agg({'Amount': 'sum'}).reset_index()
            income_expense['Income'] = df[df['Amount'] > 0].groupby('Month')['Amount'].sum().values
            income_expense['Expenses'] = df[df['Amount'] < 0].groupby('Month')['Amount'].sum().values
            
            return px.bar(
                  income_expense,
                  x='Month',
                  y=['Income', 'Expenses'],
                  barmode='group',
                  title='Total Income vs. Total Expenses'
                  ), income_expense
            
      def savings(self, df):
            return px.line(
            df,
            x='Month',
            y='Amount',
            title='Monthly Savings'
                  )