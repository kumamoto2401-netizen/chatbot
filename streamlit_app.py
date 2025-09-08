import streamlit as st
from anthropic import Anthropic

st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses Claude 3.5 Sonnet model to generate responses. "
    "Set your Anthropic API key in Streamlit secrets. "
    "Get your API key from [Anthropic Console](https://console.anthropic.com/) and set it in `.streamlit/secrets.toml`."
)

anthropic_api_key = st.secrets.get("anthropic_api_key")
if not anthropic_api_key:
    st.info(
        "Please add your Anthropic API key to your Streamlit secrets file (`.streamlit/secrets.toml`) like this:\n\n"
        "[general]\nanthropic_api_key = \"...\"\n",
        icon="🗝️"
    )
else:
    client = Anthropic(api_key=anthropic_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Convert messages to Claude format
        claude_messages = [
            {"role": "assistant" if msg["role"] == "assistant" else "user", "content": msg["content"]}
            for msg in st.session_state.messages
        ]

        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=claude_messages,
            max_tokens=1024
        )
        reply = response.content[0].text

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
