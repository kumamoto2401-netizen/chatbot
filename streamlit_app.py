import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses Gemini 2.5-flash model to generate responses. "
    "To use this app, you need to set your Google API key in Streamlit secrets. "
    "You can get an API key [here](https://makersuite.google.com/app/apikey) and set it in `.streamlit/secrets.toml`."
)

# Get Google API key from Streamlit secrets.
google_api_key = st.secrets.get("google_api_key")
if not google_api_key:
    st.info(
        "Please add your Google API key to your Streamlit secrets file (`.streamlit/secrets.toml`) like this:\n\n"
        "[general]\ngoogle_api_key = \"...\"\n",
        icon="🗝️"
    )
else:
    # Configure Gemini
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message.
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare messages for Gemini API
        history = [
            {"role": m["role"], "parts": [{"text": m["content"]}]}
            for m in st.session_state.messages
        ]

        # Generate a response using the Gemini API.
        response = model.generate_content(history)
        reply = response.text

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
