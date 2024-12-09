from create_table_sql import Brand, City, Section, Product, session
from dash import html, dash_table, dcc, Output, Input
import pandas as pd

from load_in_postgresql import get_current_date


def init_dash_table_output(dash_app) -> object:
    """
    Функция стоит таблицу промежуточный итог (page_output)
    :return: object
    """

    @dash_app.callback(
        Output("download-dataframe-xlsx", "data"),
        Input("btn_xlsx", "n_clicks"),
        prevent_initial_call=True,
    )
    def load_excel_file(n_clicks: int) -> object:
        """
        Функция отправляет файл excel в "загрузки"
        :param n_clicks: int
        :return: object
        """
        get_table = get_query()
        dataframe = pd.DataFrame(get_table)

        excel_file = dcc.send_data_frame(
            dataframe.to_excel,
            f"Парсинг {get_current_date()}.xlsx",
            sheet_name=f"Парсинг {get_current_date()}",
            index=False
        )

        return excel_file

    @dash_app.callback(
        Output('table_output', 'children'),
        Input('page-content', 'children'),
    )
    def update_table(table_output: object):
        """
        Функция строит таблицу 'ожидание парсинга'
        :param table_output: object
        :return: object
        """
        print('Таблица table_output выведена')
        result = create_table_output()
        return result

    def get_query() -> list:
        """
        Функция возвращает запрос для вывода информации после парсинга
        :return: list
        """
        get_table = ((session.query(
            Brand.name.label('Бренд'),
            City.name.label('Город'),
            Section.name.label('Секция'),
            Product.name.label('Название продукта'),
            Product.description.label('Описание'),
            Product.new_price.label('Новая цена'),
            Product.old_price.label('Старая цена'),
            Product.date.label('Дата парсинга')
        ).
                      join(Brand).
                      join(City).
                      join(Section)
                      ).
                     filter(Product.date == get_current_date()).all()
                     )
        return get_table

    def table_output_assembly(get_table) -> list[dict[str, str]]:
        """
        Функция возвращает подготовленные данные для таблицы "промежуточный итог"
        :param get_table: object
        :return: list[dict[str, str]]
        """
        output_info = []

        for row in get_table:
            brand, city, section, product_name, description, new_price, old_price, date = row

            output_info.append({
                'brand': brand,
                'city': city,
                'section': section,
                'product_name': product_name[:25] + '...' if product_name and len(product_name) >= 25 else product_name,
                'description': description[:85] + '...' if description and len(description) >= 85 else description,
                'new_price': new_price,
                'old_price': old_price,
                'date': date
            }, )
        return output_info

    def create_div_block(table_output: list[dict[str, str]], columns: list[dict]) -> html.Div:
        """
        Функция возвращает html разметку страницы
        :param table_output: list[dict[str, str]]
        :param columns: list[dict]
        :return: html.Div
        """
        div = html.Div(
            id='table_output',
            children=[
                dash_table.DataTable(
                    data=table_output,
                    columns=columns,
                    page_action="native",
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    row_selectable="multi",
                    page_current=0,
                    page_size=15,
                    style_data={
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
                                },
                ),
                html.Button("Сохранить в Excel", id="btn_xlsx"),
                dcc.Download(id="download-dataframe-xlsx")
            ],
        )
        return div

    def create_table_output() -> html.Div:
        """
        Функция возвращает страницу page_output
        :return: html.Div
        """
        columns = [
            {'name': 'Бренд', 'id': 'brand'},
            {'name': 'Город', 'id': 'city'},
            {'name': 'Секция', 'id': 'section'},
            {'name': 'Название продукта', 'id': 'product_name'},
            {'name': 'Описание', 'id': 'description'},
            {'name': 'Новая цена', 'id': 'new_price'},
            {'name': 'Старая цена', 'id': 'old_price'},
            {'name': 'Дата парсинга', 'id': 'date'}
        ]

        get_table = get_query()
        table_output = table_output_assembly(get_table)

        return create_div_block(table_output, columns)

    return create_table_output()
