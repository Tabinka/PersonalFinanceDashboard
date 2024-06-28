from dash import Dash, html

class starting_layout:
      def __init__(self, app):
            self.app = app
            
      ## create starting page for uploading file
      def render(self):
            self.app.layout = [html.Div(children='Basic Layout without input file')]