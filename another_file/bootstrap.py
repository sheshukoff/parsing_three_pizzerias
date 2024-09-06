import time
import dash
from dash import html, Input, Output, State
from dash.long_callback import DiskcacheLongCallbackManager

## Diskcache
import diskcache

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

app = dash.Dash(__name__, long_callback_manager=long_callback_manager)

app.layout = html.Div(
    [
        html.Div(
            [
                html.P(id="paragraph_id", children=["Button not clicked"]),
                html.Progress(id="progress_bar"),
            ]
        ),
        html.Button(id="button_id", children="Run Job!"),
    ]
)


# @app.long_callback(
#     output=Output("optimize-result", "children"),
#     inputs=dict(number_clicks=Input("optimize-button-id", "n_clicks")),
#     state=dict(
#         reorder_period=State("reorder-period-dropdown-id", "value"),
#         forecast=State("forecast-dropdown-id", "value")
#     ),
#     running=[
#         (Output("optimize-button-id", "disabled"), True, False),
#     ],
#     prevent_initial_call=True,
# )
# def load_optimize_data_button_click(number_clicks, reorder_period, forecast):
#     pass


@app.long_callback(
    output=Output("paragraph_id", "children"),
    inputs=Input("button_id", "n_clicks"),
    state=State("paragraph_id", "children"),
    # state=dict(
    #     reorder_period=State("paragraph_id", "children")
    # ),
    progress=[Output("progress_bar", "value")]
)
def callback(update_progress, state_a, number_clicks):
    print(update_progress, state_a, number_clicks)
    total = 10
    for i in range(total):
        time.sleep(0.5)
        update_progress((str(i + 1)))
    return [f"Clicked {number_clicks} times"]


# input


if __name__ == "__main__":
    app.run(debug=True)
