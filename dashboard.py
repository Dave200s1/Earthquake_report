import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Output, Input


class EarthquakeDashboard:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.df['time'] = pd.to_datetime(self.df['time'])
        self.df['magnitude_range'] = pd.cut(self.df['mag'], bins=[0, 3, 5, 7, 10], labels=['<3', '3-5', '5-7', '>7'])
        
        self.app = Dash(__name__)
        self.app.layout = self.create_layout()
        self.setup_callbacks()

    def create_layout(self):
        return html.Div([
            html.H1("Erdbebendaten in Japan für den Monat August", style={'textAlign': 'center'}),
            html.Div([
                html.Div([
                    dcc.Graph(id='map-plot'),
                ], className='six columns'),
                
                html.Div([
                    dcc.Graph(id='line-graph'),
                    html.Div(id='earthquake-stats', style={'margin': '20px'})
                ], className='six columns'),
            ], className='row'),
        ], className='container')

    def setup_callbacks(self):
        @self.app.callback(
            [Output('line-graph', 'figure'),
             Output('map-plot', 'figure'),
             Output('earthquake-stats', 'children')],
            Input('map-plot', 'id')  # Verwendung der ID von map-plot als Dummy-Eingabe
        )
        def update_graphs(_):
            return self.generate_graphs_and_stats()

    def generate_graphs_and_stats(self):
        # Line graph
        daily_counts = self.df.groupby(self.df['time'].dt.date).size().reset_index(name='count')
        line_fig = px.line(daily_counts, x='time', y='count', 
                           title='Anzahl der Erdbeben im Laufe der Zeit',
                           labels={'time': 'Datum', 'Aufzählung': 'Anzahl der Erdbeben'})
        line_fig.update_layout(height=400)
        
        # Map
        map_fig = go.Figure(data=go.Scattermapbox(
            lat=self.df['latitude'],
            lon=self.df['longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=self.df['mag'] * 5,
                color=self.df['mag'],
                colorscale='Viridis',
                showscale=True
            ),
            text=self.df.apply(lambda row: f"Magnitude: {row['mag']}<br>Depth: {row['depth']} km<br>Time: {row['time']}", axis=1),
            hoverinfo='text'
        ))

        map_fig.update_layout(
            mapbox_style="open-street-map",
            mapbox=dict(
                center=dict(lat=38.2682, lon=140.8694),
                zoom=4
            ),
            showlegend=False,
            height=600,
            margin={"r":0,"t":0,"l":0,"b":0}
        )
        
        # Stats
        total_earthquakes = len(self.df)
        avg_magnitude = self.df['mag'].mean()
        max_magnitude = self.df['mag'].max()
        
        stats = html.Div([
            html.H3('Erdbebenstatistik'),
            html.P(f'Insgesamt {total_earthquakes}'),
            html.P(f'Durchschnittliche Stärke: {avg_magnitude:.2f}'),
            html.P(f'Maximale Stärke: {max_magnitude:.2f}')
        ])

        return line_fig, map_fig, stats

    def run(self):
        self.app.run_server(debug=True)



    
    