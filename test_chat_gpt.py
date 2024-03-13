import dash_bootstrap_components as dbc
from dash import html, Input, Output, dash_table
import dash
from work_with_dash import data, columns

app = dash.Dash(__name__, title="Checklist Test", external_stylesheets=[dbc.themes.SLATE])

# toggle_switch_active = html.Div(
#     [
#         html.Div(
#             [
#                 dbc.Switch(
#                     id="flexSwitchCheckChecked",
#                     class_name="form-check-input",
#                     value=False,
#                 ),
#             ]
#         )
#     ]
# )

toggle_switch_active = html.Div(
    [
        dbc.Switch(
            id="active-switches-input",
            value=False,
        ),
    ],
    className='toggle_switch_active',
)

toggle_switch_disabled = html.Div(
    [
        dbc.Switch(
            id="disabled-switches-input",
            value=False,
            disabled=True,
        ),
    ],
    className='toggle_switch_disabled',
)


# pagination = html.Div([dbc.Pagination(max_value=5, first_last=True, previous_next=True)])


def check_toggle_switch(type_boolean: bool):
    if type_boolean is True:
        return toggle_switch_active
    return toggle_switch_disabled


active_page = 1
PAGE_SIZE = 15
rows = []
print(len(data))
header = [
    html.Thead(html.Tr([html.Th("Города"), html.Th("Додо"), html.Th("Ташир"), html.Th("Томато")]))
]

start = (active_page - 1) * PAGE_SIZE
end = start + PAGE_SIZE

for row in data[start:end]:
    row = html.Thead([html.Td(row['city']),
                      html.Td(check_toggle_switch(row['dodo'])),
                      html.Th(check_toggle_switch(row['tashir'])),
                      html.Th(check_toggle_switch(row['tomato']))
                      ])
    rows.append(row)

table = header + rows

app.layout = html.Div(
    children=[
        dbc.Table(table, id="table-paginated", color='dark', bordered=True),
        dbc.Pagination(
            id="pagination",
            max_value=len(data) // PAGE_SIZE + (1 if len(data) % PAGE_SIZE else 0),
            active_page=1,
            first_last=True,
        ),
    ]
)


@app.callback(
    Output("table-paginated", "children"),
    Input("pagination", "active_page"),
)
def update_table(active_page):
    start = (active_page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    header = [
        html.Thead(html.Tr([html.Th("Города"), html.Th("Додо"), html.Th("Ташир"), html.Th("Томато")]))
    ]
    rows = []
    rows.append(header)
    for row in data[start:end]:
        row = html.Thead([html.Th(row['city']),
                          html.Th(check_toggle_switch(row['dodo'])),
                          html.Th(check_toggle_switch(row['tashir'])),
                          html.Th(check_toggle_switch(row['tomato']))
                          ])
        rows.append(html.Thead([html.Td(cell) for cell in row]))

    table = header + rows
    return table


if __name__ == "__main__":
    app.run_server(debug=True)

# @app.callback(
#     Output("standalone-radio-check-output", "children"),
#     Input("standalone-switch", "value"),
# )
# def on_form_change(switch_checked):
#     return switch_checked

#
# [
#     dbc.Table(
#         header + rows,
#         id="table-paginated",
#         bordered=True,
#         color='dark',
#         size='md',
#     ),
#     dbc.Pagination(
#         id="pagination",
#         max_value=len(data) // PAGE_SIZE + (1 if len(data) % PAGE_SIZE else 0),
#         active_page=1,
#         # size=15,
#         first_last=True,
#         previous_next=True,
#     ),
# ]
# className,
# class_name,
# disabled,
# id,
# inputClassName,
# inputStyle,
# input_class_name,
# input_style,
# label,
# labelClassName,
# labelStyle,
# label_class_name,
# label_id,
# label_style,
# loading_state,
# name,
# persisted_props,
# persistence,
# persistence_type,
# style,
# value


# switches = html.Div(
#     [
#         dbc.Label("Toggle a bunch"),
#         dbc.Checklist(
#             options=[
#                 {"label": "Option 1", "value": 1},
#                 {"label": "Option 2", "value": 2},
#                 {"label": "Disabled Option", "value": 3, "disabled": True},
#             ],
#             value=[1],
#             id="switches-input",
#             switch=True,
#         ),
#     ]
# )
