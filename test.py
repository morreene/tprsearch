import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Label("Select value:", className="text-end", style={'paddingRight': '10px'})
        ], width=2, className="align-self-center"),
        dbc.Col([
            dcc.RangeSlider(
                id='my-range-slider',
                min=0.5,
                max=1,
                step=0.1,
                value=[0.7, 1],
                marks={
                    0.5: '0.5',
                    0.6: '0.6',
                    0.7: '0.7',
                    0.8: '0.8',
                    0.9: '0.9',

                    1: '1'
                },
                className="mx-0 px-0"  # Remove margin/padding
            )
        ], width=10)
    ]),
    html.Div(id='slider-output-container')
])

@app.callback(
    Output('slider-output-container', 'children'),
    Input('my-range-slider', 'value')
)
def update_output(value):
    selected_range = [round(i / 10, 1) for i in range(int(value[0] * 10), 11)]
    return 'You have selected: {}'.format(value[0])

@app.callback(
    Output('my-range-slider', 'value'),
    Input('my-range-slider', 'value')
)
def update_slider(value):
    return [value[0], 1]

if __name__ == '__main__':
    app.run_server(debug=True)
