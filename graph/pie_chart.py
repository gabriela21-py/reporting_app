import pandas as pd
from dash.dependencies import Output, Input
from plotly.graph_objs import Figure
from dash import dcc, html
import plotly.express as px

from graph.chart_interface import Chart

class PieChart(Chart):
    def __init__(self, title, app, chart_id, value_column, label_column, database, custom_query):
        super().__init__(title, app, chart_id, database)
        self.issue_type = None
        self.current_filter = None
        self.value_column = value_column
        self.label_column = label_column
        self.custom_query = custom_query
        self.callbacks()

    def get_data(self) -> pd.DataFrame:
        return self.database.get_data(self.custom_query)

    def generate_query(self, filter_value: str | list[str]) -> str:
        filters = []
        if self.issue_type:
            filters.append(f"issue_type = '{self.issue_type}'")

        if isinstance(filter_value, list) and filter_value:
            teams = "', '".join(filter_value)
            filters.append(f"agile_team IN ('{teams}')")
        elif isinstance(filter_value, str) and filter_value != "all":
            filters.append(f"agile_team = '{filter_value}'")

        where_clause = " AND ".join(filters)

        return f"""
            SELECT COUNT(*) AS {self.value_column}, {self.label_column}
            FROM jira_snapshot
            WHERE {where_clause}
            GROUP BY {self.label_column}
        """

    def set_filter_value(self, value: str):
        self.current_filter = value
        self.custom_query = self.generate_query(value)


    def get_layout(self):
        return html.Div([
            html.H3(self.title),
            dcc.Graph(
                id=self.chart_id,
                style={
                    'height': '350px',
                    'width': '100%',
                    'minWidth': '300px',
                    'maxWidth': '600px',
                    'margin': '0 auto',
                },
                config={
                    'responsive': False,
                    'displayModeBar': False
                }
            )
        ], style={
            'width': '100%',
            'textAlign': 'center',
            'boxSizing': 'border-box',
            'overflow': 'visible'
        })


    def create_figure(self, df: pd.DataFrame) -> Figure:
        fig = px.pie(
            df,
            values=self.value_column,
            names=self.label_column,
            title=self.title,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig.update_traces(
            textinfo='percent+label',
            hoverinfo='label+value+percent',
            hoverlabel=dict(
                font_size=11,
                font_family="Arial"
            )
        )
        return fig


    def update_chart(self) -> Figure:
        df = self.get_data()
        return self.create_figure(df)


    def callbacks(self):
        @self.app.callback(
            Output(self.chart_id, "figure"),
            Input("chart-filter", "value"),
            prevent_initial_call=False
        )
        def _callback(selected_value):
            value = selected_value or "all"
            self.set_filter_value(value)
            return self.update_chart()
