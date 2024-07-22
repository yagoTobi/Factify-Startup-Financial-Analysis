import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import tiktoken
from tiktoken._educational import *

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    style={
        "background-color": "#001f3f",
        "height": "100vh",
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
    },
    children=[
        html.Div(
            style={
                "background-color": "white",
                "width": "85%",
                "aspect-ratio": "16/9",
                "display": "flex",
            },
            children=[
                # Column 1
                html.Div(
                    style={
                        "width": "75%",
                        "padding": "20px",
                        "display": "flex",
                        "flex-direction": "column",
                    },
                    children=[
                        dcc.Textarea(
                            id="text-input",
                            style={
                                "width": "100%",
                                "height": "40%",
                                "margin-bottom": "20px",
                            },
                            placeholder="Type your prompt here...",
                        ),
                        html.Div(
                            id="tokenized-output",
                            style={
                                "width": "100%",
                                "height": "60%",
                                "overflow-y": "scroll",
                                "background-color": "#f0f0f0",
                                "padding": "10px",
                            },
                        ),
                    ],
                ),
                # Column 2
                html.Div(
                    style={
                        "width": "25%",
                        "padding": "20px",
                        "display": "flex",
                        "flex-direction": "column",
                    },
                    children=[
                        dcc.Dropdown(
                            id="model-selector",
                            options=[
                                {"label": "Model 1", "value": "model_1"},
                                {"label": "Model 2", "value": "model_2"},
                            ],
                            value="model_1",
                            style={"margin-bottom": "20px"},
                        ),
                        html.Div(id="model-info", style={"margin-bottom": "20px"}),
                        html.Div(id="price-output"),
                    ],
                ),
            ],
        )
    ],
)


def tokenize_text(text):
    enc = SimpleBytePairEncoding.from_tiktoken("cl100k_base")
    tokens = enc.encode(text)
    token_texts = enc.decode(tokens)
    return tokens, token_texts


@app.callback(Output("tokenized-output", "children"), [Input("text-input", "value")])
def update_output(text):
    if not text:
        return ""

    tokens, token_texts = tokenize_text(text)
    spaced_text = "  ".join(token_texts)
    print(tokens)
    return html.Div(
        [dcc.Markdown(token_texts)],
        style={"white-space": "pre-wrap", "word-wrap": "break-word"},
    )


# Define pricing per model (example values)
pricing = {
    "model_1": 0.0001,  # price per token for model 1
    "model_2": 0.0002,  # price per token for model 2
}

model_info = {
    "model_1": "Price per token: $0.0001",
    "model_2": "Price per token: $0.0002",
}


@app.callback(Output("model-info", "children"), [Input("model-selector", "value")])
def update_model_info(model):
    return model_info.get(model, "")


@app.callback(
    Output("price-output", "children"),
    [Input("text-input", "value"), Input("model-selector", "value")],
)
def calculate_price(text, model):
    if not text or not model:
        return ""

    tokens, _ = tokenize_text(text)
    num_tokens = len(tokens)
    price = num_tokens * pricing[model]

    return f"Number of tokens: {num_tokens}, Price: ${price:.4f}"


if __name__ == "__main__":
    app.run_server(debug=True)
