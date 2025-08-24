from flask import Flask, render_template
import dash
from dash import html

from dashboard import get_layout, register_callbacks
from database.postgres import PostgresDatabase
from graph.donut_chart import DonutChart
from graph.pie_chart import PieChart
from graph.table import StatusPriorityTable
from config import PROBLEM_QUERY, PRIORITY_QUERY, SEVERITY_QUERY


server = Flask(__name__)
app = dash.Dash(__name__, assets_folder="static", server=server, url_base_pathname="/dashboard/")

db = PostgresDatabase()
app.layout = get_layout(app, db)
register_callbacks(app, db)
@server.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    server.run(debug=True)
