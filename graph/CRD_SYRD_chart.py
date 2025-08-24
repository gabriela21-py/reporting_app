from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure

from graph.chart_interface import Chart


class CRDChart(Chart):
    def __init__(self, title, app, chart_id, database, value_column, label_column, color_map=None):
        super().__init__(title, app, chart_id, database)
        self.value_column = value_column
        self.label_column = label_column
        self.color_map = color_map or {}
        self.callbacks()

    def generate_query(self, filter_field=None, filter_value=None) -> str:
        condition = f"WHERE crd.{filter_field} = '{filter_value}'" if filter_field and filter_value else ""
        return f"""
            WITH crd_syrd_status AS (
                SELECT
                    crd.id AS crd_id,
                    COUNT(syrd.crd_id) AS total_syrds,
                    SUM(CASE WHEN LOWER(TRIM(syrd.syrd_state)) = 'released' THEN 1 ELSE 0 END) AS released_syrds
                FROM
                    public.crd
                LEFT JOIN
                    public.syrd ON crd.id = syrd.crd_id
                {condition}
                GROUP BY
                    crd.id
            )
            SELECT
                COUNT(*) FILTER (WHERE total_syrds > 0 AND total_syrds = released_syrds) AS implemented_count,
                COUNT(*) FILTER (WHERE total_syrds = 0 OR total_syrds <> released_syrds) AS not_implemented_count
            FROM
                crd_syrd_status;
        """

    def get_layout(self):
        return html.Div([
            html.H3(self.title),
            dcc.Graph(
                id=self.chart_id,
                style={
                    'height': '350px',
                    'width': '550px',
                    'minWidth': '300px',
                    'maxWidth': '600px',
                    'margin': '0 auto',
                },
                config={'responsive': False, 'displayModeBar': False}
            )
        ])

    def create_figure(self, df: pd.DataFrame) -> Figure:
        total = df[self.value_column].sum()
        fig = px.pie(
            df,
            values=self.value_column,
            names=self.label_column,
            hole=0.5,
            color=self.label_column,
            color_discrete_map=self.color_map
        )
        fig.update_traces(
            textinfo='percent+label',
            hovertemplate="%{label}<br><b>Count</b>: %{value}<br><b>Percent</b>: %{percent}",
        )
        fig.update_layout(
            annotations=[{
                "text": f"SYRD<br>{total}",
                "x": 0.5, "y": 0.5,
                "font_size": 12,
                "showarrow": False
            }],
            showlegend=True
        )
        return fig

    def update_filtered_chart(self, filter_field, filter_value):
        query = self.generate_query(filter_field, filter_value)
        raw_df = self.database.get_data(query)
        print("Filter field:", filter_field)
        print("Filter value:", filter_value)
        df = pd.DataFrame({
            self.label_column: ["Implemented", "Not Implemented"],
            self.value_column: [
                raw_df.iloc[0]["implemented_count"],
                raw_df.iloc[0]["not_implemented_count"]
            ]
        })
        return self.create_figure(df)

    def update_chart(self) -> Figure:
        return self.update_filtered_chart(None, None)

    def callbacks(self):
        @self.app.callback(
            Output(self.chart_id, "figure"),
            Input("filter-mode", "value"),
            Input("filter-value", "value"),
            prevent_initial_call=False
        )
        def _callback(filter_field, filter_value):
            return self.update_filtered_chart(filter_field, filter_value)
