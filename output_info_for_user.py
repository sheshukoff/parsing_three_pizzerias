from create_table_sql import Brand, City, Section, Product, session
from dash import Dash, html, dcc, dash_table, Input, Output, callback
from flask import Flask

flask_app = Flask(__name__)

dash_app_output = Dash(
    __name__,
    server=flask_app,
    suppress_callback_exceptions=True,
    requests_pathname_prefix='/output_info_for_user/'
)

dash_app_output.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# @callback(Output('page-content', 'children'),
#           [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/output_info_for_user':
#         return page_output_info
#     else:
#         "404"


get_table = (session.query(
    Brand.name, City.name, Section.name, Product.name, Product.description, Product.new_price, Product.old_price
).join(Brand).join(City).join(Section)).all()

output_info = []

for row in get_table:
    brand, city, section, product_name, description, new_price, old_price = row

    output_info.append({
        'brand': brand,
        'city': city,
        'section': section,
        'product_name': product_name,
        'description': description,
        'new_price': new_price,
        'old_price': old_price
    }, )

columns = [
    {'name': 'Бренд', 'id': 'brand'},
    {'name': 'Город', 'id': 'city'},
    {'name': 'Секция', 'id': 'section'},
    {'name': 'Название продукта', 'id': 'product_name'},
    {'name': 'Описание', 'id': 'description'},
    {'name': 'Новая цена', 'id': 'new_price'},
    {'name': 'Старая цена', 'id': 'old_price'},
]

page_output_info = html.Div(
    [
        dash_table.DataTable(
            data=output_info,
            columns=columns,
            page_action="native",
            page_current=0,
            page_size=15,
            style_header={'backgroundColor': '#161a1d', 'fontWeight': 'bold',
                          'color': '#a0a1ab', 'border': '1px solid black', 'font-family': 'Noto Kufi Arabic'},
            style_table={'height': '670px', 'overflow': 'hidden', 'width': '100%', 'margin': 'auto'},
            style_cell={'padding': '5px', 'fontSize': 16, 'font-family': 'Noto Kufi Arabic', 'textAlign': 'left',
                        'border': '2px solid grey', 'backgroundColor': '#161a1d', 'color': '#a0a1ab'},
            style_cell_conditional=[
                {'if': {'column_id': 'Бренд'},
                 'width': '10%'},
                {'if': {'column_id': 'Город'},
                 'width': '10%'},
                {'if': {'column_id': 'Секция'},
                 'width': '10%'},
                {'if': {'column_id': 'Название продукта'},
                 'width': '10%'},
                {'if': {'column_id': 'Описание'},
                 'width': '40%'},
                {'if': {'column_id': 'Новая цена'},
                 'width': '10%'},
                {'if': {'column_id': 'Старая цена'},
                 'width': '10%'},
            ],
        )
    ]
)
