from dash import Dash, html

class basic_layout:
      def __init__(self, data, app):
            self.data = data
            self.app = app

      def start_page(self):
            self.app.layout = [html.Div(children='Input file loaded')]