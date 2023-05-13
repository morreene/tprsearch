import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
from flask import Flask, request, redirect, url_for, flash, session, render_template_string

import pandas as pd
import openai
import pandas as pd
from openai.embeddings_utils import get_embedding, cosine_similarity

import webbrowser
from threading import Timer


API_KEY = "3842bbdef12e406dbaf407d7a133ee7e"
RESOURCE_ENDPOINT = "https://openai-mais.openai.azure.com/"

openai.api_type = "azure"
openai.api_key = API_KEY
openai.api_base = RESOURCE_ENDPOINT
openai.api_version = "2022-12-01"



# search docs with openai embedding
def search_docs(df, user_query, top_n=3, to_print=False):
    embedding = get_embedding(
        user_query,
        engine="text-embedding-ada-002" # engine should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model
    )
    df["similarities"] = df.ada_v2.apply(lambda x: cosine_similarity(x, embedding))

    res = (
        df.sort_values("similarities", ascending=False)
        .head(top_n)
    )
    if to_print:
        print(res)
    return res





# Load the data
df = pd.read_csv("data/my_data.csv")
# tpr = pd.read_parquet(r'data/tpr_embedding_for_dash_app_openai_ada_v2.parquet')
# tpr = pd.read_feather(r'data/tpr_embedding_for_dash_app_openai_ada_v2.feather')
tpr = pd.read_pickle(r'data/tpr_embedding_for_dash_app_openai_ada_v2.pickle')

# Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Define the Dash app
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/', suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
# external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

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
    <h2>Login</h2>
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





#################################################
# Start the function page
#################################################

index_page = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                [
                    dbc.NavLink('About', id='open-offcanvas', href='#'),
                    dbc.Offcanvas([
                            dcc.Markdown(
                                '''
                                    This document search engine incorporates a new search feature that utilizes text embeddings from OpenAI's large language model, 
                                    providing more accurate and relevant search results. Here's an explanation of what this means and how it differs from traditional search methods.

                                    ##### What are text embeddings?

                                    Text embeddings can be thought of as a way to convert complex language into a simpler, mathematical representation that computers 
                                    can understand more easily. By representing words, phrases, and paragraphs as points in a high-dimensional space, text embeddings 
                                    enable our search engine to process and interpret the meaning of the text more effectively.

                                    ##### How is this search different from traditional text matching search?

                                    Traditional search engines often rely on matching keywords or phrases from your search query to those found in documents. While this 
                                    method has its merits, it can sometimes miss the true meaning or context behind the words being used.

                                    This new search feature, powered by text embeddings from OpenAI's large language model, takes a more sophisticated approach. By converting 
                                    both your search query and the documents into embeddings, we can measure the similarity between them in the high-dimensional space. 
                                    This allows our search engine to better understand the meaning and context of the words, phrases, and sentences, providing more relevant 
                                    and accurate results that better align with your intentions.

                                    ##### How should you construct your query?

                                    Be clear and specific when crafting your query. There's no need to worry about whether the words or phrases will exactly match the text 
                                    you want to find. The search engine will focus on understanding the meaning behind your query and deliver relevant results accordingly.

                                    You can use English, French, Spanish, Arabic, German and other languages.                                    
                                '''
                                ),
                    ],
                        id="offcanvas",
                        backdrop=True,
                        title="Understanding Search Based on Text Embeddings",
                        is_open=False,
                        placement='end'
                    ),
                ]
            ),
            dbc.NavItem(dbc.NavLink("Logout", href="#", id='logout-button')),
            html.Div(id='dummy-output'),  # Dummy output to trigger the callback
        ],
        brand="TPR Reports - AI-Powered Search",
        brand_href="/dashboard/",
        color="primary",
        dark=True,
    ),

    html.Br(),

    dbc.Row([
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
    ], justify="center", id='top-space'),

    dbc.Row([
            dbc.Col(
                    dbc.InputGroup([
                            dbc.Input(id="search-box", type="text", placeholder="Enter search query, e.g. subsidies and government support to fossil feul and energy", ),
                            dbc.Button(" Search ", id="search-button", 
                                            #    className="btn btn-primary mt-3", 
                                            n_clicks=0),
                    
                    ]
                ), width=6,
            ),
    ], justify="center", className="header", id='search-container'),

    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col([

            dcc.Markdown(
                '''
                Based on reports issued after 2015 for 119 Members

                Search query examples:
                * subsidies and government supports on fossil fuel and energy
                * الإعانات والدعم الحكومي للوقود الأحفوري والطاقة
                * interdictions d'importer ou d'exporter
                * Πολιτικές που ευνοούν τις μικρές επιχειρήσεις
                * find policies related to MSME, SME or small businesses in Africa
                * any competition policy related to high-tech sector
                * quantatitive restrictions (with typo)
                * policies supporting ecommerce

                    
                '''
                ),



        ], width=5),
    ], justify="center", className="header", id='sample-queries'),

    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col([
            html.Div(id="search-results", className="results"),
        ], width=9),
    ], justify="center", className="header"),
])


@dash_app.callback(
        [Output("search-results", "children"),  
         Output("top-space", "style"),
         Output("sample-queries", "style")
         
         
         ],
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
        # matches = df[df.apply(lambda row: search_terms in str(row), axis=1)]

        matches = search_docs(tpr, search_terms, top_n=500)
        # matches = tpr.head(200)
        # matches['similarities']=0.8569125155
        matches['similarities']=matches['similarities'].round(3)


        matches = matches[['Symbol','ReportMemberName','IssuingDate','Topic', 'text','similarities']]
        matches.columns = ['Symbol','Member','Date','Section/Topic','Text (Paragraph)','Score']

    else:
        matches = df

    # Display the results in a datatable
    return dbc.Container([
            dash_table.DataTable(
                    # id='tab',
                    # columns=[
                    #     {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns if i != 'ID'
                    # ],
                    # data = dff.to_dict('records'),
                    id="search-results-table",
                    columns=[{"name": col, "id": col} for col in matches.columns],
                    data=matches.to_dict("records"),


                    editable=False,
                    filter_action="native",

                    sort_action="native",
                    sort_mode="multi",
                    
                    column_selectable=False,
                    row_selectable=False,
                    row_deletable=False,
                    
                    selected_columns=[],
                    selected_rows=[],
                    
                    page_action="native",
                    page_current= 0,
                    page_size= 20,

                    style_header={'fontWeight': 'bold'},

                    style_cell={
                        'height': 'auto',
                        # 'minWidth': '50px', 
                        # 'maxWidth': '800px',
                        'width': '100px',
                        'whiteSpace': 'normal',
                        'textAlign': 'left',
                        'fontSize': '14px',
                        'verticalAlign': 'top'
                    },
                    style_cell_conditional=[
                        {'if': {'column_id': 'Symbol'},
                         'width': '50px'},
                        {'if': {'column_id': 'Member'},
                         'width': '90px'},
                        {'if': {'column_id': 'Date'},
                         'width': '80px'},
                        {'if': {'column_id': 'Section/Topic'},
                         'width': '200px'},
                        {'if': {'column_id': 'Text (Paragraph)'},
                         'width': '600px'},
                        {'if': {'column_id': 'Score'},
                         'width': '80px', 'textAlign': 'right'},
                    ],
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(250, 250, 250)',
                        }
                    ],
                    style_as_list_view=True,
                )
            ]), {'display': 'none'}, {'display': 'none'}

#################################################
# end of function page
#################################################


# toggle offcanvas help
@dash_app.callback(
    Output("offcanvas", "is_open"),
    [Input("open-offcanvas", "n_clicks"), 
    #  Input("offcanvas-close", "n_clicks")
     ],
    [dash.dependencies.State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open





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







# original
if __name__ == '__main__':
    app.run(debug=True)
    # app.run_server(debug=True)



# # for pyinstaller
# def open_browser():
# 	webbrowser.open_new("http://localhost:{}/dashboard/".format(5000))

# if __name__ == '__main__':
#     Timer(1, open_browser).start();
#     dash_app.run_server(debug=False, port=5000)





