import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, dcc
import dash
from work_with_dash import data

app = dash.Dash(__name__, title="Checklist Test", external_stylesheets=[dbc.themes.SLATE])

# ... [Оставь существующий код без изменений до этого момента] ...

# Предположим, что у тебя есть переменная 'data' с данными для таблицы
# и переменная 'PAGE_SIZE' с размером страницы.

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


def check_toggle_switch(type_boolean: bool):
    if type_boolean is True:
        return toggle_switch_active
    return toggle_switch_disabled


active_page = 1
PAGE_SIZE = 15
rows = []
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
        dbc.Table(
            # ... [Таблица, как раньше] ...
            table,
            id="table-paginated",
            bordered=True,
            color="primary",
        ),
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
    rows = []
    for row in data[start:end]:
        row = [row['city'],
               check_toggle_switch(row['dodo']),
               check_toggle_switch(row['tashir']),
               check_toggle_switch(row['tomato'])]
        rows.append(html.Tr([html.Td(cell) for cell in row]))
    return rows


# ... [Оставь остальную часть кода без изменений] ...
if __name__ == "__main__":
    app.run_server(debug=True)
