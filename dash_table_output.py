from create_table_sql import Brand, City, Section, Product, session
from dash import html, dash_table


def init_dash_table_output() -> object:
    """
    Функция стоит таблицу промежуточный итог (page_output)
    :return: object
    """
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

    return html.Div(
        children=[
            dash_table.DataTable(
                data=output_info,
                columns=columns,
                page_action="native",
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable="multi",
                page_current=0,
                page_size=15,
                tooltip_duration=500,
                tooltip_data=[
                    {
                        column: {'value': str(value), 'type': 'markdown'}
                        for column, value in row.items()
                    } for row in output_info
                ],
                style_data={
                    # 'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_header={'backgroundColor': '#161a1d',
                              'fontWeight': 'bold',
                              'color': '#FFFFFF',
                              'border': '1px solid black',
                              'font-family': 'Noto Kufi Arabic'
                              },
                style_table={'height': '670px',
                             'overflow': 'auto',
                             'width': '100%',
                             'margin': 'auto'},
                style_cell={'padding': '5px',
                            'fontSize': 16,
                            'font-family': 'Noto Kufi Arabic',
                            'textAlign': 'left',
                            'border': '2px solid grey',
                            'backgroundColor': '#161a1d',
                            'color': '#a0a1ab',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 0},
                style_cell_conditional=[
                    {'if': {'column_id': 'Бренд'},
                        'width': '5%'},
                    {'if': {'column_id': 'Город'},
                     'width': '5%'},
                    {'if': {'column_id': 'Секция'},
                     'width': '5%'},
                    {'if': {'column_id': 'Название продукта'},
                     'width': '10%'},
                    {'if': {'column_id': 'Описание'},
                     'width': '30%'},
                    {'if': {'column_id': 'Новая цена'},
                     'width': '5%'},
                    {'if': {'column_id': 'Старая цена'},
                     'width': '5%'},
                ],
            )
        ]
    )
