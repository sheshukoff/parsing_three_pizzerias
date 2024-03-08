import dash_bootstrap_components as dbc
from dash import html, Input, Output
import dash
from work_with_dash import data


app = dash.Dash(__name__, title="Checklist Test")


toggle_switch_active = html.Div(
    [
        html.Div(
            [
                dbc.Switch(
                    id="standalone-switch",
                    value=False,
                ),
            ]
        ),
        html.P(id="standalone-radio-check-output"),
    ]
)

toggle_switch_disabled = html.Div(
    [
        html.Div(
            [
                dbc.Switch(
                    id="standalone-switch",
                    disabled=True,
                ),
            ]
        ),
        html.P(id="standalone-radio-check-output"),
    ]
)


def check_toggle_switch(type_boolean: bool):
    if type_boolean is True:
        return toggle_switch_active
    return toggle_switch_disabled


rows = []

for row in data:
    # print(row['city'], row['dodo'], row['tashir'], row['tomato'])
    row = [row['city'],
           check_toggle_switch(row['dodo']),
           check_toggle_switch(row['tashir']),
           check_toggle_switch(row['tomato'])]
    rows.append(row)


@app.callback(
    Output("standalone-radio-check-output", "children"),
    Input("standalone-switch", "value"),
)
def on_form_change(switch_checked):
    return f"Selections: Toggle Switch: {switch_checked}"


app.layout = html.Div(
    [
        dbc.Table(
            # using the same table as in the above example
            [html.Tr([html.Td(cell) for cell in row]) for row in rows],
            bordered=True,
            id="table-color",
            color="primary",
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)

