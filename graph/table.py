import pandas as pd
from dash import html, dash_table
from dash.dependencies import Input, Output

class StatusPriorityTable:
    def __init__(self, app, table_id, database):
        self.app = app
        self.table_id = table_id
        self.database = database
        self.callbacks()

    def get_data(self, filter_value=None) -> pd.DataFrame:
        team_filter=""
        if isinstance(filter_value, list) and filter_value:
            team_list = "', '".join(filter_value)
            team_filter = f" AND agile_team IN ('{team_list}')"
        elif isinstance(filter_value, str) and filter_value:
            team_filter = f" AND agile_team = '{filter_value}'"
        query = f"""
                SELECT
                    jira_status AS status,
                    COUNT(CASE WHEN priority = 'Blocking' THEN 1 END) AS Blocking,
                    COUNT(CASE WHEN priority = 'High' THEN 1 END) AS High,
                    COUNT(CASE WHEN priority = 'Low' THEN 1 END) AS Low,
                    COUNT(CASE WHEN priority = 'Medium' THEN 1 END) AS Medium,
                    COUNT(*) AS Total
                FROM jira_snapshot
                WHERE issue_type = 'Problem Report'
                {team_filter}
                GROUP BY jira_status
                ORDER BY jira_status;
        """
        df = self.database.get_data(query)

        total_row = df.select_dtypes(include='number').sum()
        total_row['status'] = 'Total'
        df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)

        return df

    def get_layout(self):
        return html.Div([
            html.H3("Open PRs by Priority and Status"),
            dash_table.DataTable(
                id=self.table_id,
                columns=[],
                data=[],
                style_cell={'textAlign': 'center', 'padding': '5px'},
                style_header={
                    'backgroundColor': 'lightgrey',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    },
                    {
                        'if': {
                            'filter_query': '{status} = "Total"'
                        },
                        'backgroundColor': '#d3d3d3',
                        'fontWeight': 'bold'
                    }
                ]
            )

        ])

    def callbacks(self):
        @self.app.callback(
            Output(self.table_id, 'data'),
            Output(self.table_id, 'columns'),
            Input("chart-filter", 'value')
        )
        def update_table(filter_value):
            if not filter_value:
                filter_value = None
            df = self.get_data(filter_value)
            columns = [{"name": col, "id": col} for col in df.columns]
            data = df.to_dict('records')
            return data, columns
