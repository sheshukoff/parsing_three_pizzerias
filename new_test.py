import flask
import dash
from dash import dcc
from dash import html

app = dash.Dash(__name__)
app.secret_key = "some secret petelka_458"

app.layout = html.Form([
    html.H1('Страница 1'),
    html.P('Сначала нужно заполнить поле'),
    dcc.Input(name='name'),
    html.Button('Submit', type='submit')
], action='/page_2', method='post')


# page_2_layout = html.Form([
#     html.H1('Страница 2'),
#     dcc.Input(name='name'),
#     html.Button('Submit', type='submit')
# ], action='/', method='post')


@app.server.route('/page_2', methods=['POST'])
def on_post():
    data = flask.request.form
    row = dict(data)
    column = row['name']
    if len(column) == 0:
        print(column)
        return flask.redirect('/')
    else:
        print(column)
        return flask.redirect('/page_2')


if __name__ == '__main__':
    app.run_server(debug=True, port=7779)
