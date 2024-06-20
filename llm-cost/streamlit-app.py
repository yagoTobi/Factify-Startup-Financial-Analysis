import streamlit as st
import random
import tiktoken
from tiktoken._educational import *


# Define the tokenize_text function
def tokenize_text(text):
    enc = tiktoken.encoding_for_model("gpt-4o")
    tokens = enc.encode(text)
    token_texts = enc.decode(tokens)
    return tokens, token_texts


# Define random color function
def random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"


# Define pricing per model (example values)
pricing = {
    "model_1": 0.0001,  # price per token for model 1
    "model_2": 0.0002,  # price per token for model 2
}

model_info = {
    "model_1": "Price per token: $0.0001",
    "model_2": "Price per token: $0.0002",
}

# Streamlit page configuration
st.set_page_config(page_title="Tokenization App", layout="wide")

# Layout
col1, col2 = st.columns([3, 1])

with col1:
    st.header("Input your prompt")
    text_input = st.text_area("Type your prompt here...", key="text-input")
    submit_button = st.button("Submit")

    if submit_button and text_input:
        tokens, token_texts = tokenize_text(text_input)
        print(token_texts)
        tokenized_output = " ".join(
            f"<span style='color: {random_color()};'>{token}</span>"
            for token in token_texts
        )

        st.markdown("## Tokenized Output")
        st.markdown(
            f"<div style='background-color: #f0f0f0; padding: 10px; height: 200px; overflow-y: scroll;'>{tokenized_output}</div>",
            unsafe_allow_html=True,
        )

with col2:
    st.header("Model Selection")
    model_selector = st.selectbox(
        "Select model:", ["model_1", "model_2"], key="model-selector"
    )

    if model_selector:
        st.markdown("## Model Info")
        st.markdown(model_info[model_selector])

        if submit_button and text_input:
            num_tokens = len(tokens)
            price = num_tokens * pricing[model_selector]

            st.markdown(f"## Token Count")
            st.markdown(f"Number of tokens: {num_tokens}")

            st.markdown(f"## Price Calculation")
            st.markdown(f"Price: ${price:.4f}")


def random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"


if __name__ == "__main__":
    st.set_option("deprecation.showPyplotGlobalUse", False)
    st.title("Tokenization App")
    st.write("This app tokenizes text and calculates the cost based on selected model.")
