import dash
# import dash_core_components as dcc
# import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
from flask import Flask, request, redirect, url_for, flash, session, render_template_string
import pandas as pd


# Load the data
df = pd.read_csv("my_data.csv")


app = Flask(__name__)
app.secret_key = 'your-secret-key'


# Define the Dash app


dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/', suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

users = {'wto': 'wto','w': 'w',}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['user'] = username
            return redirect('/dashboard/')
        else:
            flash('Invalid credentials')
            return redirect('/login')
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
        <style>
      body {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        padding: 0;
        font-family: Arial, sans-serif;
      }
      form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 20px;
        background-color: #f5f5f5;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
      }
      input[type="text"],
      input[type="password"] {
        padding: 10px;
        margin: 5px;
        border: none;
        border-radius: 3px;
        box-shadow: 0 0 3px rgba(0, 0, 0, 0.2);
      }
      input[type="submit"] {
        padding: 10px;
        margin: 5px;
        background-color: #4caf50;
        background-color: #0d6efd;
        color: white;
        border: none;
        border-radius: 3px;
        cursor: pointer;
      }
      h1 {
        margin-bottom: 20px;
      }
    </style>
</head>
<body>
    <h1>Login</h1>
    <form action="/login" method="post">
        <label for="username">Username:</label>
        <input type="text" name="username" id="username">
        <br>
        <label for="password">Password:</label>
        <input type="password" name="password" id="password">
        <br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
    ''')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.before_request
def before_request():
    if 'user' not in session and request.endpoint != 'login':
        return redirect('/login')

















# Start the function page



index_page = html.Div([
    dbc.NavbarSimple(
    children=[
        # dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.NavItem(dbc.NavLink("Logout", href="#", id='logout-button')),
        # html.Button('Logout', id='logout-button'),
        html.Div(id='dummy-output'),  # Dummy output to trigger the callback


        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem("More pages", header=True),
        #         dbc.DropdownMenuItem("Page 2", href="#"),
        #         dbc.DropdownMenuItem("Page 3", href="#"),
                
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="More",
        # ),
    ],
    brand="Search TPR Reports",
    brand_href="#",
    color="primary",
    dark=True,
    # expand ='lg',
    # fluid =True,
),

    # html.Div([
    #     html.Div(className="search-box-container", children=[
    #         dcc.Input(id="search-box", type="text", placeholder="Enter search terms...", className="search-box"),
    #         html.Button("Search", id="search-button", className="search-button"),
    #     ])
    # ], className="header"),
    # html.Div(id="search-results", className="results"),
    html.Br(),
    html.Br(),

    # dbc.Row([
    #         # dbc.Col(
    #         #     dbc.Input(type="password", placeholder="Enter password"),
    #         #     className="me-3",width=4,
    #         # ),
    #         # dbc.Col(dbc.Button("Submit", color="primary"), width="auto"),

    #         dbc.Col(
    #             # dbc.Input(type="password", placeholder="Enter password"),

    #         html.H1('Search Engine', 
    #                 # className="title"
    #                 ),

    #             className="me-3",width=4,
    #         ),


    # ], justify="center", className="header"),

    dbc.Row([
            html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),


    ], justify="center", className="header", id='top_space'),


    dbc.Row([
        
            dbc.Col(
                dbc.Input(id="search-box", type="text", placeholder="Enter search terms...", 
                        #   className="form-control"
                          ),
                className="me-3",width=4,
            ),
            dbc.Col(
                # dbc.Button("Submit", color="primary"), width="auto",
                dbc.Button("Search", id="search-button", 
                        #    className="btn btn-primary mt-3", 
                           n_clicks=0),width="auto",
            ),
    ], justify="center", className="header", id='search-container'),

        html.Br(),
            html.Br(),




    # dbc.Row([
    #     dbc.Col([
            
    #         dbc.Form([
    #             dbc.Input(id="search-box", type="text", placeholder="Enter search terms...", className="form-control"),
    #             dbc.Button("Search", id="search-button", className="btn btn-primary mt-3", n_clicks=0),
    #         ]),
    #     ], width=6),
    # ], justify="center", className="header"),

    dbc.Row([
        dbc.Col([
            html.Div(id="search-results", className="results"),


        ], width=9),
    ], justify="center", className="header"),

    # dcc.Input(id='input', value='Enter something', type='text'),
    # html.Div(id='output'),
    # html.Br(),
    # html.Button('Logout', id='logout-button'),
    # html.Div(id='dummy-output')  # Dummy output to trigger the callback
])

@dash_app.callback(Output('output', 'children'), [Input('input', 'value')])
def update_value(value):
    return f'You have entered: {value}'

@dash_app.callback(
        [Output("search-results", "children"),  Output("top_space", "style")],
        [Input("search-button", "n_clicks")], 
        [State("search-box", "value")])
def search(n_clicks, search_terms):
    # Check if the search button was clicked
    # if n_clicks is None:
    #     return None
    if n_clicks <=0 or search_terms=='' or search_terms is None:
        return "", {'display': 'block'}

    # Search the dataframe for matching rows
    if search_terms:
        matches = df[df.apply(lambda row: search_terms in str(row), axis=1)]
    else:
        matches = df

    # Display the results in a datatable
    return dbc.Container([
                dash_table.DataTable(
                    id="search-results-table",
                    columns=[{"name": col, "id": col} for col in matches.columns],
                    data=matches.to_dict("records"),
                    filter_action="native",
                    sort_action="native",
                    style_table={"overflowX": "scroll"},
                )
            ]), {'display': 'none'}



# # Define the app layout
# index_page = html.Div([
#     html.H1("Search Engine", className="title"),
#     html.Div([
#         html.Div(className="search-box-container", children=[
#             dcc.Input(id="search-box", type="text", placeholder="Enter search terms...", className="search-box"),
#             html.Button("Search", id="search-button", className="search-button"),
#         ])
#     ], className="header"),
#     html.Div(id="search-results", className="results"),
#     html.Button('Logout', id='logout-button'),
# ])

# # Define the callback to handle search box input
# @dash_app.callback(Output("search-results", "children"), [Input("search-button", "n_clicks")], [State("search-box", "value")])
# def search(n_clicks, search_terms):
#     # Check if the search button was clicked
#     if n_clicks is None:
#         return None

#     # Search the dataframe for matching rows
#     if search_terms:
#         matches = df[df.apply(lambda row: search_terms in str(row), axis=1)]
#     else:
#         matches = df

#     # Display the results in a datatable
#     return dash_table.DataTable(
#         id="search-results-table",
#         columns=[{"name": col, "id": col} for col in matches.columns],
#         data=matches.to_dict("records"),
#         filter_action="native",
#         sort_action="native",
#         style_table={"overflowX": "scroll"},
#     )






# dash_app.clientside_callback(
#     """
#     function(search_clicks) {
#         if (search_clicks > 0) {
#             return {'top': '20px', 'position': 'fixed'};
#         }
#         return {'top': '33%', 'position': 'fixed'};
#     }
#     """,
#     Output('search-container', 'style'),
#     Input('search-button', 'n_clicks')
# )














# end of function page





@dash_app.callback(Output('dummy-output', 'children'), [Input('logout-button', 'n_clicks')])
def logout_dash(n):
    if n:
        session.pop('user', None)
        return dcc.Location(pathname='/logout', id='dummy-location', refresh=True)

def serve_layout():
    if 'user' in session:
        return index_page
    return html.Div()

dash_app.layout = serve_layout

if __name__ == '__main__':
    app.run(debug=True)
