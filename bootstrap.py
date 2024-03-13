import dash
from dash import html, Input, Output, ALL
import dash_bootstrap_components as dbc
import pandas as pd
from work_with_dash import data


# определяем класс Cell, который имеет два атрибута: is_checked и is_boolean
class Cell:
    def __init__(self, is_checked=False, is_enabled=True):
        self.is_checked = is_checked # определяем, выбран ли чекбокс
        self.is_enabled = is_enabled # определяем, есть ли чекбокс в ячейке

    def to_checklist(self, col, row):
        # преобразуем объект cell в объект dbc.Checklist
        if self.is_enabled: # если есть чекбокс в ячейке
            return dbc.Checklist(
                options=[
                    {
                        "label": "",
                        "value": f"col_{col}_row_{row}",
                    }
                ],
                id={
                    "type": "checkboxes",
                    "index": f"col_{col}_row_{row}",
                },
                switch=True, # делаем чекбоксы в виде переключателей
                value=[f"col_{col}_row_{row}"] if self.is_checked else [], # устанавливаем значение чекбокса в зависимости от атрибута is_checked
            )
        else: # если нет чекбокса в ячейке
            return "" # возвращаем пустую строку

    def __repr__(self):
        return f'{str(self.is_checked), self.is_enabled}'
    #     return f'[is_checked={str(self.is_checked)}, is_enabled={str(self.is_enabled)}]'


rows = []
for city in data:
    row = [Cell(False, city['dodo']), Cell(False, city['tashir']), Cell(False, city['tomato'])]
    rows.append(row)

# print(*rows, sep='\n')




# создаем список из строк и столбцов с объектами Cell
# rows = []
# for column_number in range(0, 4):
#     row = []
#     for row_number in range(0, 4):
#         # создаем объект Cell с случайными значениями атрибутов
#         import random
#         is_checked = random.choice([True, False])
#         is_boolean = random.choice([True, False])
#         cell_obj = Cell(False, is_boolean)
#         row.append(cell_obj)
#     rows.append(row)
# print(*rows, sep='\n')

for i, row in enumerate(rows, 1):
    for j, cell_obj in enumerate(row, 1):
        print(cell_obj)


# преобразуем список объектов cell в список объектов dbc.Checklist
# rows = [[cell_obj.to_checklist(j, i) for j, cell_obj in enumerate(row, 1)] for i, row in enumerate(rows, 1)]

app = dash.Dash(__name__, title="Checklist Test")


app.layout = html.Div(
    [
        dbc.Table( # создаем таблицу из списка строк
            [html.Tr([html.Td(cell) for cell in row]) for row in rows],
            striped=True,
            bordered=True,
            hover=True,
            responsive=True,
        ),
        html.Div([], id="output_info"),
    ]
)


@app.callback(
    Output("output_info", "children"),
    Input({"type": "checkboxes", "index": ALL}, "value"),
)
def update_div(value_in):
    changed_values = [x[0] for x in value_in if isinstance(x, list) and len(x) > 0]
    if len(changed_values) > 0:
        return [", ".join(changed_values)]
    else:
        return ["No Checkboxes"]

#
# if __name__ == "__main__":
#     app.run_server(debug=True)
