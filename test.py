import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Create a DataFrame with some dummy data
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [24, 30, 35, 19],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
})

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Input(id="input", placeholder="Type something...", type="text"),
    dbc.Button("Search", id='button', n_clicks=0),
    html.Div(id='output-container-button', children='Enter a name and press "Search"')
])

@app.callback(
    Output('output-container-button', 'children'),
    Input('button', 'n_clicks'),
    State('input', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        results = df[df['Name'] == value]
        if results.empty:
            return 'No results found'
        else:
            return results.to_dict('records')
    else:
        return 'Enter a name and press "Search"'

if __name__ == "__main__":
    app.run_server(debug=True)