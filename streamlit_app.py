import streamlit as st
from anthropic import Anthropic

st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses Claude-3 to generate responses. "
    "Set your Anthropic API key in Streamlit secrets. "
    "Get your API key from [Anthropic Console](https://console.anthropic.com/) and set it in `.streamlit/secrets.toml`."
)

# システムプロンプトの設定
SYSTEM_PROMPT = "You are a helpful AI assistant. Please provide clear and concise responses."

anthropic_api_key = st.secrets.get("anthropic_api_key")
if not anthropic_api_key:
    st.info(
        "Please add your Anthropic API key to your Streamlit secrets file (`.streamlit/secrets.toml`) like this:\n\n"
        "[general]\nanthropic_api_key = \"sk-ant-xxx...\"\n",
        icon="🗝️"
    )
else:
    try:
        client = Anthropic(api_key=anthropic_api_key)

        if "messages" not in st.session_state:
            st.session_state.messages = [{
                "role": "assistant",
                "content": "Hello! How can I help you today?"
            }]

        # チャット履歴の表示
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # チャット入力
        if prompt := st.chat_input("What is up?"):
            # ユーザーメッセージをチャット履歴に追加
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            try:
                # API用のメッセージ準備（システムプロンプトは別パラメータとして渡す）
                api_messages = []
                for msg in st.session_state.messages:
                    if msg["role"] in ["user", "assistant"]:
                        api_messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })

                # Claude API呼び出し
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",  # 最新の利用可能なモデルを使用
                    messages=api_messages,
                    system=SYSTEM_PROMPT,
                    temperature=0.7,
                    max_tokens=1024
                )

                # レスポンス処理
                if response.content and len(response.content) > 0:
                    reply = response.content[0].text
                    with st.chat_message("assistant"):
                        st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    st.error("No response received from Claude")

            except Exception as e:
                st.error(f"Error in API call: {str(e)}")
                st.error("Please check your API key and try again.")

    except Exception as e:
        st.error(f"Failed to initialize Anthropic client: {str(e)}")
