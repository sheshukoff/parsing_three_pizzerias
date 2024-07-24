from flask import Flask

from another_file.new_test import make_dash, make_layout, define_callbacks

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


dash_app = make_dash(app)
dash_app.layout = make_layout()
define_callbacks()

if __name__ == '__main__':
    app.run(debug=True)
