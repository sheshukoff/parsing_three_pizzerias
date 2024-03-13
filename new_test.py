import dash
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.exceptions import PreventUpdate

# 1) this is needed to use emojis:
# -*- coding: utf-8 -*-

# # table with task and employees
# df_selection = pd.DataFrame(columns = ['Row','Column'])
#
# df_selection.to_csv('last_selected.csv')

# 2) table with task and employees with unselected boxes
df = pd.DataFrame(
    columns=['Task', 'Employee 1', 'Employee 2', 'Employee 3', 'Employee 4', 'Employee 5', 'Employee 6', 'Employee 7',
             'Employee 8'])
df['Task'] = ["Task 1 ", "Task 2", "Task 3", "Task 4"]
df['Employee 1'] = ['⬜', '⬜', '⬜', '⬜']
df['Employee 2'] = ['⬜', '⬜', '⬜', '⬜']
df['Employee 3'] = ['⬜', '⬜', '⬜', '⬜']
df['Employee 4'] = ['⬜', '⬜', '⬜', '⬜']
df['Employee 5'] = ['⬜', '⬜', '⬜', '⬜']
df['Employee 6'] = ['⬜', '⬜', '⬜', '⬜']
df['Employee 7'] = ['⬜', '⬜', '⬜', '⬜']
df['Employee 8'] = ['⬜', '⬜', '⬜', '⬜']

# create the tables to show the inforamtion:
table = html.Div([
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        editable=False,
        style_data_conditional=[
            {'if': {'state': 'active'}, 'backgroundColor': 'white', 'border': '1px solid white'},
        ],
        style_as_list_view=True,
        column_selectable='single',
        id='table',
        style_data={"font-size": "14px", 'width': 15, "background": "white", 'text-align': 'center'},
    )
])

app = dash.Dash(__name__)

# Layout of the page:
app.layout = html.Div([
    html.H2("Employees Tasks"),
    html.H4("All Tasks are empty", id="Message1"),
    html.Div(table, style={'width': '60%'}),
])


# Callbacks
@app.callback(Output("Message1", "children"),
              Output("table", "data"),
              [Input('table', 'active_cell'),
               State('table', 'data')])
def update_loosers(cell, data):
    # If there is not selection:
    if not cell:
        raise PreventUpdate
    else:
        # If the user select a box:
        # 3) takes the info for the row and column selected
        row_selected = cell["row"]
        row_name = data[row_selected]["Task"]
        column_selected = cell["column"]
        column_name = cell["column_id"]
        message = "Check a box"

        # 4) Change the figure of the box selected
        if data[row_selected][column_name] == '+':
            data[row_selected][column_name] = '⬜'
            message = "The " + row_name + " of the " + column_name + " has been unselected"

        elif data[row_selected][column_name] == '⬜':
            data[row_selected][column_name] = '+'
            message = "The " + row_name + " of the " + column_name + " has been completed"
            print(column_name, row_name)
        return message, data


if __name__ == "__main__":
    app.run_server(debug=True)
