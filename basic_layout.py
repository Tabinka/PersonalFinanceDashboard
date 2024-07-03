import pandas as pd
from dash import dcc, html, dash_table, Output

class BasicLayout:
      def __init__(self, data, app):
            self.data = data
            self.app = app
            self.app.layout = self.start_page()

      def start_page(self):
            if 'Amount' in self.data.columns:
                  self.data['Amount'] = self.data['Amount'].astype(float)  # Convert to float, adjust as needed
            return html.Div([
                  html.H5("Render saved file"),

                  dash_table.DataTable(
                        self.data.to_dict('records'),
                        [{'name': i, 'id': i} for i in self.data.columns]
                  ),

                  html.Hr(),  # horizontal line
            ])
            
      def register_callbacks(self):
            @self.app.callback(
                  Output('income-expense-chart', 'figure'),
                  Output('expense-category-pie-chart', 'figure'),
                  Output('monthly-savings-chart', 'figure'),
                  Output('expense-trends-chart', 'figure'),
                  Output('top-expenses-table', 'data')
            )
            def update_output():
                  if self.data is not None:
                        df = self.data
                        # Data preprocessing
                        df['Date'] = pd.to_datetime(df['Date'])
                        df['Month'] = df['Date'].dt.to_period('M')