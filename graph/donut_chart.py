import pandas as pd
from dash.dependencies import Output, Input
from plotly.graph_objs import Figure
from dash import dcc, html
import plotly.express as px

from graph.chart_interface import Chart
from graph.pie_chart import PieChart


class DonutChart(PieChart):
    def __init__(self, title, app, chart_id, value_column, label_column, database, custom_query, issue_type):
        super().__init__(title, app, chart_id, value_column, label_column, database, custom_query)
        self.custom_query = custom_query
        self.issue_type = issue_type

    def create_figure(self, df: pd.DataFrame) -> Figure:
        total = df[self.value_column].sum()
        fig = px.pie(
            df,
            values=self.value_column,
            names=self.label_column,
            title=self.title,
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig.update_traces(
            textinfo='percent+label',
            hovertemplate="%{label}<br><b>Valoare</b>: %{value}<br><b>Procent</b>: %{percent}",
            hoverlabel=dict(
                font_size=13,
                font_family="Arial"
            )
        )
        fig.update_layout(
            annotations=[{
                "text": f"Total: {total}",
                "x": 0.5, "y": 0.5,
                "font_size": 10,
                "showarrow": False
            }]
        )
        return fig

