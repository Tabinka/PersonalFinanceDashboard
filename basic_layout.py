from dash import dcc, html, dash_table
from starting_layout import StartingLayout

class BasicLayout:
      def __init__(self, data, app):
            self.data = data
            self.app = app
            self.app.layout = self.start_page()

      def start_page(self):
            if 'Amount' in self.data.columns:
                  self.data['Amount'] = self.data['Amount'].astype(float)  # Convert to float, adjust as needed
            return html.Div([
                  html.H5("Render file"),

                  dash_table.DataTable(
                        self.data.to_dict('records'),
                        [{'name': i, 'id': i} for i in self.data.columns]
                  ),

                  html.Hr(),  # horizontal line
            ])