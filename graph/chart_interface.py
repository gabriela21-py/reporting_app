from abc import ABC, abstractmethod
import pandas as pd
from dash import dcc, html, Input, Output
from plotly.graph_objs import Figure

from database.db_interface import DatabaseInterface
from database.postgres import PostgresDatabase

class Chart(ABC):
    def __init__(self, title, app, chart_id, database:DatabaseInterface):
        self.query = None
        self.title = title
        self.app = app
        self.chart_id = chart_id
        self.database = database

    @abstractmethod
    def create_figure(self, data: pd.DataFrame) -> Figure:
        pass

    @abstractmethod
    def get_layout(self):
        pass

    @abstractmethod
    def update_chart(self) -> Figure:
        pass

    def get_data(self) -> pd.DataFrame:
        return self.database.get_data(self.query)

    def callbacks(self):
        @self.app.callback(
            Output(self.chart_id, "figure"),
            [Input(self.chart_id, "clickData")]
        )
        def _callback(clickData):
            return self.update_chart()
