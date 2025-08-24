from dash import Output, Input
from plotly.graph_objs import Figure
from graph.CRD_SYRD_chart import CRDChart
import pandas as pd


class SyRDStateChart(CRDChart):
    def __init__(self, title, app, chart_id, database, value_column, label_column, color_map=None):
        super().__init__(title, app, chart_id, database, value_column, label_column, color_map)
    def generate_query(self, filter_field=None, filter_value=None) -> str:
        condition = f"WHERE {filter_field} = '{filter_value}'" if filter_field and filter_value else ""
        return f"""
            SELECT 
                syrd_state AS status,
                COUNT(*) AS count
            FROM SyRD
            {condition}
            GROUP BY syrd_state
            ORDER BY count DESC;
        """

    def update_filtered_chart(self, filter_field, filter_value) -> Figure:
        df = self.database.get_data(self.generate_query(filter_field, filter_value))
        return self.create_figure(df)

    def callbacks(self):
        @self.app.callback(
            Output(self.chart_id, "figure"),
            Input("filter-mode", "value"),
            Input("filter-value", "value"),
            prevent_initial_call=False
        )
        def _callback(filter_field, filter_value):
            return self.update_filtered_chart(filter_field, filter_value)
