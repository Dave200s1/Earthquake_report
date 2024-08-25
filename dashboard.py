import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash
import os

class Earthquake_Dashboard:
    def __init__(self,csv_file):
        self.app = dash.Dash(__name__)
        self.df = self.load_data()
        self.setup_layout()
        self.setup_callbacks(
        )
        
    def load_data(self, file_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_dir, 'query.csv')
        df = pd.read_csv(csv_path)
        # time in datetime konventieren 
        df['time'] = pd.to_datetime(df['time'])
        # Create magnitude ranges
        df['magnitude_range'] = pd.cut(df['mag'], bins=[0, 3, 5, 7, 10], labels=['<3', '3-5', '5-7', '>7'])
        return df
    
    def setup_layout(self):
        self.app.layout = html.Div([
    html.H1("Earthquake Data in Japan"),
    
    dcc.Graph(id='pie-chart'),
    
    dcc.Graph(id='map-plot')
])
    
    
    def create_pie_chart(self):
        magnitude_counts = self.df['magnitude_range'].value_contains()
        fig = px.pie(
            values= magnitude_counts.values,
            names = magnitude_counts.index
            title = 'Distribution of Earthquake Magnitudes near Japan'
        )
        return fig
    
    def setup_callbacks(self):
        @self.app.callback(
            Output('pie-chart', 'figure'),
            Input('pie_chart', 'id')
        )
        def update_pie_chart(self):
            return self.create_pie_chart()
            
        
    def run(self):
        pass
    
    