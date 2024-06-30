from dash import dcc, html, dash_table, Input, Output, State, callback
import base64
import datetime
import io

import pandas as pd

class StartingLayout:
      def __init__(self, app):
            self.app = app
            self.app.layout = self.render()
            self.register_callbacks()
            
      ## create starting page for uploading file
      def render(self):
            return html.Div([
                  dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                              'Drag and Drop or ',
                              html.A('Select Files')
                        ]),
                        style={
                              'width': '100%',
                              'height': '60px',
                              'lineHeight': '60px',
                              'borderWidth': '1px',
                              'borderStyle': 'dashed',
                              'borderRadius': '5px',
                              'textAlign': 'center',
                              'margin': '10px'
                        },
                        # Allow multiple files to be uploaded
                        multiple=False
                  ),
                  html.Div(id='output-data-upload'),
                  ])
            
      def parse_contents(self, contents, filename):
            content_type, content_string = contents.split(',')

            decoded = base64.b64decode(content_string)
            try:
                  if 'csv' in filename:
                        # Assume that the user uploaded a CSV file
                        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                  elif 'xls' in filename:
                        # Assume that the user uploaded an excel file
                        df = pd.read_excel(io.BytesIO(decoded))
                  
                  # just for testing input, subject to change when dealing with real data
                  if 'Amount' in df.columns:
                        df['Amount'] = df['Amount'].astype(float)  # Convert to float, adjust as needed
            except Exception as e:
                  print(e)
                  return html.Div([
                        'There was an error processing this file.'
                  ])

            return html.Div([
                  html.H5(filename),

                  dash_table.DataTable(
                        df.to_dict('records'),
                        [{'name': i, 'id': i} for i in df.columns]
                  ),

                  html.Hr(),  # horizontal line

                  # For debugging, display the raw contents provided by the web browser
                  html.Div('Raw Content'),
                  html.Pre(contents[0:200] + '...', style={
                        'whiteSpace': 'pre-wrap',
                        'wordBreak': 'break-all'
                  })
            ])
            
      def register_callbacks(self):
            @self.app.callback(
                  Output('output-data-upload', 'children'),
                  Input('upload-data', 'contents'),
                  State('upload-data', 'filename')
            )
            def update_output(list_of_contents, list_of_names):
                  if list_of_contents is not None and list_of_names is not None:
                        # Ensure they are lists
                        if not isinstance(list_of_contents, list):
                              list_of_contents = [list_of_contents]
                        if not isinstance(list_of_names, list):
                              list_of_names = [list_of_names]
                        
                        children = [
                              self.parse_contents(c, n) for c, n in
                              zip(list_of_contents, list_of_names)
                        ]
                        return children