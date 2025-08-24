from dash import html, dcc, Input, Output
from config import PROBLEM_QUERY, PRIORITY_QUERY, SEVERITY_QUERY, UPDATE_DROPDOWN_QUERY, FEATURES_QUERY
from graph.donut_chart import DonutChart
from graph.syrd_state_chart import SyRDStateChart
from graph.table import StatusPriorityTable
from graph.test_case_chart import TestCaseChart
from utils import create_dropdown
from graph.CRD_SYRD_chart import CRDChart


def get_layout(app, db):
    problem_chart = DonutChart(
        title="Problem Report Tickets",
        app=app,
        chart_id="problem-donut",
        value_column="count",
        label_column="jira_status",
        database=db,
        custom_query=PROBLEM_QUERY,
        issue_type="Problem Report"
    )

    priority_chart = DonutChart(
        title="Priority Report Tickets",
        app=app,
        chart_id="priority-donut",
        value_column="count",
        label_column="priority",
        database=db,
        custom_query=PRIORITY_QUERY,
        issue_type="Problem Report"
    )

    severity_chart = DonutChart(
        title="Severity Report Tickets",
        app=app,
        chart_id="severity-donut",
        value_column="count",
        label_column="severity",
        database=db,
        custom_query=SEVERITY_QUERY,
        issue_type="Problem Report"
    )

    features_chart = DonutChart(
        title="Features Report Tickets",
        app=app,
        chart_id="features-donut",
        value_column="count",
        label_column="jira_status",
        database=db,
        custom_query=FEATURES_QUERY,
        issue_type="Story"
    )

    implementation_chart = CRDChart(
        title="Implemented Requirements (Filtered)",
        app=app,
        chart_id="impl-donut",
        database=db,
        value_column="count",
        label_column="status",
        color_map={
            "Implemented": "#27ae60",
            "Not Implemented": "#e67e22"
        }
    )

    testcase_chart = TestCaseChart(
        title="Sys+Sw Requirements with Test Cases",
        app=app,
        chart_id="syrd-testcase-donut",
        database=db,
        value_column="count",
        label_column="status",
        color_map={
            "With Test Case": "#27ae60",
            "Without Test Case": "#f57c00"
        }
    )

    syrd_state_chart = SyRDStateChart(
        title="SyRD Requirements by State",
        app=app,
        chart_id="syrd-state-donut",
        database=db,
        value_column="count",
        label_column="status",
        color_map={
            "released": "#27ae60",
            "draft": "#f39c12",
            "review": "#3498db",
            "archived": "#7f8c8d"
        }
    )

    status_table = StatusPriorityTable(app=app, table_id="table", database=db)

    dropdown = create_dropdown(
        id="chart-filter",
        multi=True,
        placeholder="All Teams"
    )

    dropdown_crd_filter = create_dropdown(
        id="filter-mode",
        options=[
            {"label": "Test Level", "value": "test_level"},
            {"label": "Requirement Level", "value": "requirement_level"}
        ],
        placeholder="Select Filter Type",
        value=None
    )

    dropdown_filter_value = create_dropdown(
        id="filter-value",
        placeholder="Select Filter Value",
        className = "dropdown-with-margin"
    )

    app_layout = html.Div([
        html.Div([
            html.H1("Dashboard", className="dashboard-title"),
            dropdown,
        ], className="header-container"),

        html.Div([
            html.Div(problem_chart.get_layout(), className="box"),
            html.Div(priority_chart.get_layout(), className="box")
        ], className="row"),

        html.Div([
            html.Div(severity_chart.get_layout(), className="box"),
            html.Div(status_table.get_layout(), className="box")
        ], className="row"),

        html.Div([
            html.Div(features_chart.get_layout(), className="box"),
        ], className="row"),

        html.Div([
            html.H1("CRD Requirements", className="dashboard-title"),
            dropdown_crd_filter,
            dropdown_filter_value
        ], className = "header-container"),

        html.Div([
            html.Div(implementation_chart.get_layout(), className="box"),
            html.Div(testcase_chart.get_layout(), className="box"),
        ], className="row" , style={"marginTop": "80px"}),

        html.Div([
            html.Div(syrd_state_chart.get_layout(), className="box"),
        ], className="row")
    ], className = "main-container")

    return app_layout



def register_callbacks(app, db):
    @app.callback(
        Output("chart-filter", "value"),
        Output("chart-filter", "options"),
        Input("chart-filter", "id")
    )
    def update_dropdown_value_and_data(selected_value):
        query = UPDATE_DROPDOWN_QUERY
        df = db.get_data(query)
        teams = df["agile_team"].tolist()

        options = [{"label": team, "value": team} for team in teams]
        selected = selected_value if selected_value in teams else "All Teams"
        return selected, options

    @app.callback(
        Output("filter-value", "options"),
        Input("filter-mode", "value")
    )
    def update_filter_value_options(filter_field):
        if not filter_field:
            return []

        query = f"""
            SELECT DISTINCT {filter_field}
            FROM crd
            WHERE {filter_field} IS NOT NULL
            ORDER BY {filter_field};
        """
        df = db.get_data(query)
        return [{"label": val, "value": val} for val in df[filter_field].dropna()]
