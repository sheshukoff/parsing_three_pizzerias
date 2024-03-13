import dash_bootstrap_components as dbc
from dash import html, Input, Output
import dash
from work_with_dash import data

table_header = [
    html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
]

row1 = html.Tr([html.Td("Arthur"), html.Td("Dent")])
row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")])
row4 = html.Tr([html.Td("Trillian"), html.Td("Astra")])

table_body = [html.Tbody([row1, row2, row3, row4])]

table = dbc.Table(table_header + table_body, bordered=True)


app = dash.Dash(__name__, title="Checklist Test")


app.layout = html.Div(
    [
        dbc.Table(
            # using the same table as in the above example
            table_header + table_body,
            id="table-color",
            color="primary",
        ),
    ]
)

if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(debug=True)


