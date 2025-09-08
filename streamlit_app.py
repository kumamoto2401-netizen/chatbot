import streamlit as st
import google.generativeai as genai

st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses Gemini 2.5-flash model to generate responses. "
    "Set your Google API key in Streamlit secrets. "
    "API key is [here](https://makersuite.google.com/app/apikey) and set it in `.streamlit/secrets.toml`."
)

google_api_key = st.secrets.get("google_api_key")
if not google_api_key:
    st.info(
        "Please add your Google API key to your Streamlit secrets file (`.streamlit/secrets.toml`) like this:\n\n"
        "[general]\ngoogle_api_key = \"...\"\n",
        icon="🗝️"
    )
else:
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Geminiへの入力は配列または文字列のみ
        # roleやpartsは不要
        chat_history = [m["content"] for m in st.session_state.messages]

        response = model.generate_content(chat_history)
        reply = response.text

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
