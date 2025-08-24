from dash import Output, Input

from graph.CRD_SYRD_chart import CRDChart
import pandas as pd


class TestCaseChart(CRDChart):
    def __init__(self, title, app, chart_id, database, value_column, label_column, color_map=None):
        super().__init__(title, app, chart_id, database, value_column, label_column, color_map)
    def generate_query(self, filter_field=None, filter_value=None) -> str:
        condition = f"WHERE s.{filter_field} = '{filter_value}'" if filter_field and filter_value else ""
        return f"""
            SELECT 
                CASE 
                    WHEN tc.id IS NULL THEN 'Without Test Case'
                    ELSE 'With Test Case'
                END AS status,
                COUNT(DISTINCT s.id) AS count
            FROM syrd s
            LEFT JOIN testcase tc ON s.id = tc.syrd_id
            {condition}
            GROUP BY status;
        """

    def update_filtered_chart(self, filter_field, filter_value):
        df = self.database.get_data(self.generate_query(filter_field, filter_value))

        data = {
            "With Test Case": 0,
            "Without Test Case": 0
        }
        for _, row in df.iterrows():
            data[row["status"]] = row["count"]

        final_df = pd.DataFrame({
            self.label_column: list(data.keys()),
            self.value_column: list(data.values())
        })

        return self.create_figure(final_df)

    def callbacks(self):
        @self.app.callback(
            Output(self.chart_id, "figure"),
            Input("filter-mode", "value"),
            Input("filter-value", "value"),
            prevent_initial_call=False
        )
        def _callback(filter_field, filter_value):
            return self.update_filtered_chart(filter_field, filter_value)
