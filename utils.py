from dash import dcc

def create_dropdown(
        **kwargs,
) -> dcc.Dropdown:
    style = {
        "width": "300px",
        "margin-left": "auto",
        "margin-right": "auto",
        "margin-bottom": "auto"
    }
    return dcc.Dropdown(style=style, **kwargs)
