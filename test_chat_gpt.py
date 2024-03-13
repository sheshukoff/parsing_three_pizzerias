import dash_bootstrap_components as dbc
from dash import html, Input, Output, callback
import dash
from work_with_dash import data

app = dash.Dash(__name__, title="Checklist Test", external_stylesheets=[dbc.themes.SLATE])

PAGE_SIZE = 15

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


def get_total_page(page_size, total_data):
    data_div_page_size = total_data // page_size
    data_mod_page_size = total_data % page_size
    total_page = data_div_page_size if data_mod_page_size == 0 else (data_div_page_size + 1)

    return total_page


def get_data_pagination(part_table):
    table_header = [
        html.Thead(
            html.Tr([
                html.Th("Города"),
                html.Th("Додо"),
                html.Th("Ташир"),
                html.Th("Томато"),
            ])
        )
    ]

    table_rows = []
    for row in part_table:
        table_row = html.Tr([
            html.Td(row['city']),
            html.Td(check_toggle_switch(row['dodo'])),
            html.Td(check_toggle_switch(row['tashir'])),
            html.Td(check_toggle_switch(row['tomato'])),
        ])
        table_rows.append(table_row)

    table_body = [html.Tbody(table_rows)]

    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True, className='p-3')

    return table


@callback(
    Output('score-list', 'children'),
    Input('pagination', 'active_page'),
)
def table_pagination(active_page):
    start = (active_page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE

    part_table = data[start:end]
    table = get_data_pagination(part_table)

    return table


# active_page = 3
# PAGE_SIZE = 15
# rows = []
# header = [
#     html.Thead(html.Tr([html.Th("Города"), html.Th("Додо"), html.Th("Ташир"), html.Th("Томато")]))
# ]
#
# start = (active_page - 1) * PAGE_SIZE
# end = start + PAGE_SIZE
#
# print(start, end)
#
# for row in data[start:end]:
#     row = html.Tr([html.Td(row['city']),
#                    html.Td(check_toggle_switch(row['dodo'])),
#                    html.Td(check_toggle_switch(row['tashir'])),
#                    html.Td(check_toggle_switch(row['tomato']))
#                    ])
#     rows.append(row)
#
# table_body = [html.Tbody(rows)]
#
# table = header + table_body

# @callback(
#     Output('score-list', 'children'),
#     Input('pagination', 'active_page'),
# )
# def update_list_scores(page):
#     # convert active_page data to integer and set default value to 1
#     int_page = 1 if not page else int(page)
#
#     # define filter index range based on active page
#     filter_index_1 = (int_page - 1) * PAGE_SIZE
#     filter_index_2 = (int_page) * PAGE_SIZE
#
#     # get data by filter range based on active page number
#     fitler_scores = top_100_scores[filter_index_1:filter_index_2]
#
#     # load data to dash bootstrap table component
#     table = get_student_score_list(fitler_scores, (filter_index_1 + 1))
#
#     return table


# pagination = html.Div([dbc.Pagination(id="pagination",
#                                       active_page=1,
#                                       min_value=1,
#                                       max_value=len(data) // PAGE_SIZE + (1 if len(data) % PAGE_SIZE else 0),
#                                       first_last=True,
#                                       )])

app.layout = html.Div(
    [
        dbc.Table(id="score-list"),
        dbc.Pagination(id="pagination",
                       max_value=get_total_page(PAGE_SIZE, len(data)),
                       fully_expanded=False)
    ],
)


# @callback(
#     Output('score-list', 'children'),
#     Input('pagination', 'active_page'),
# )
# def update_table(active_page):


# @app.callback(
#     Output("pagination-contents", "children"),
#     [Input("pagination", "active_page")],
# )
# def change_page(page):
#     if page:
#         return f"Page selected: {page}"
#     return "Select a page"

# @app.callback(
#     Output("table-paginated", "children"),
#     Input("pagination", "active_page"),
# )
# def update_table(active_page):
#     start = (active_page - 1) * PAGE_SIZE
#     end = start + PAGE_SIZE
#     header = [
#         html.Thead(html.Tr([html.Th("Города"), html.Th("Додо"), html.Th("Ташир"), html.Th("Томато")]))
#     ]
#     rows = []
#     rows.append(header)
#     for row in data[start:end]:
#         row = html.Thead([html.Th(row['city']),
#                           html.Th(check_toggle_switch(row['dodo'])),
#                           html.Th(check_toggle_switch(row['tashir'])),
#                           html.Th(check_toggle_switch(row['tomato']))
#                           ])
#         rows.append(html.Thead([html.Td(cell) for cell in row]))
#
#     table = header + rows
#     return table


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

# @callback(
#     Output('score-list', 'children'),
#     Input('pagination', 'active_page'),
# )
# def update_list_scores(page):
#     # convert active_page data to integer and set default value to 1
#     int_page = 1 if not page else int(page)
#
#     # define filter index range based on active page
#     filter_index_1 = (int_page - 1) * PAGE_SIZE
#     filter_index_2 = (int_page) * PAGE_SIZE
#
#     # get data by filter range based on active page number
#     fitler_scores = top_100_scores[filter_index_1:filter_index_2]
#
#     # load data to dash bootstrap table component
#     table = get_student_score_list(fitler_scores, (filter_index_1 + 1))
#
#     return table


# def get_total_page(page_size, total_data):
#     data_div_page_size = total_data // page_size
#     data_mod_page_size = total_data % page_size
#     total_page = data_div_page_size if data_mod_page_size == 0 else (data_div_page_size + 1)
#
#     return total_page

# dbc.Table(id="score-list"),
# dbc.Pagination(id="pagination", max_value=get_total_page(PAGE_SIZE, 100), fully_expanded=False)
