import json
import logging
import streamlit as st  # 1.34.0
import time
import tiktoken

from datetime import datetime

# from openai import OpenAI  # 1.30.1
from openai import AzureOpenAI  # 1.30.1

logger = logging.getLogger()
logging.basicConfig(encoding="UTF-8", level=logging.INFO)

st.title("🤩 Improved Streamlit Chat UI")

# To be used with standard OpenAI API
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# To be used with standard Azure OpenAI API
client = AzureOpenAI(
    azure_endpoint=st.secrets["OPENAI_API_ENDPOINT"],
    api_key=st.secrets["OPENAI_API_KEY"],
    api_version="2024-02-15-preview",
)


# This function logs the last question and answer in the chat messages
def log_feedback(icon):
    # We display a nice toast
    st.toast("Thanks for your feedback!", icon="👌")

    # We retrieve the last question and answer
    last_messages = json.dumps(st.session_state["messages"][-2:])

    # We record the timestamp
    activity = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": "

    # And include the messages
    activity += "positive" if icon == "👍" else "negative"
    activity += ": " + last_messages

    # And log everything
    logger.info(activity)


# Model Choice - Name to be adapter to your deployment
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-35-turbo"

# Adapted from https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if len(st.session_state["messages"]) < 8:

    user_avatar = "👩‍💻"
    assistant_avatar = "🤖"

    # In case of rerun of the last question, we remove the last answer from st.session_state["messages"]
    if "rerun" in st.session_state and st.session_state["rerun"]:

        st.session_state["messages"].pop(-1)

    # We rebuild the previous conversation stored in st.session_state["messages"] with the corresponding emojis
    for message in st.session_state["messages"]:
        with st.chat_message(
            message["role"],
            avatar=assistant_avatar if message["role"] == "assistant" else user_avatar,
        ):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I help you?"):

        st.session_state["messages"].append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar=user_avatar):
            st.markdown(prompt)

    if prompt or ("rerun" in st.session_state and st.session_state["rerun"]):

        with st.chat_message("assistant", avatar=assistant_avatar):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state["messages"]
                ],
                stream=True,
                max_tokens=300,
            )
            response = st.write_stream(stream)
        st.session_state["messages"].append({"role": "assistant", "content": response})

        if "rerun" in st.session_state and st.session_state["rerun"]:
            st.session_state["rerun"] = False

    if len(st.session_state["messages"]) > 0:

        cols_dimensions = [7, 19.4, 19.3, 9, 8.6, 8.6, 28.1]
        col0, col1, col2, col3, col4, col5, col6 = st.columns(cols_dimensions)

        with col1:

            # Converts the list of messages into a JSON Bytes format
            json_messages = json.dumps(st.session_state["messages"]).encode("utf-8")

            st.download_button(
                label="📥 Save chat!",
                data=json_messages,
                file_name="chat_conversation.json",
                mime="application/json",
            )

        with col2:
            if st.button("Clear Chat 🧹"):
                st.session_state["messages"] = []
                st.rerun()

        with col3:
            icon = "🔁"
            if st.button(icon):
                st.session_state["rerun"] = True
                st.rerun()

        with col4:
            icon = "👍"
            if st.button(icon):
                log_feedback(icon)

        with col5:
            icon = "👎"
            if st.button(icon):
                log_feedback(icon)

        with col6:
            enc = tiktoken.get_encoding("cl100k_base")
            tokenized_full_text = enc.encode(
                " ".join([item["content"] for item in st.session_state["messages"]])
            )
            label = f"💬 {len(tokenized_full_text)} tokens"
            st.link_button(label, "https://platform.openai.com/tokenizer")

    else:

        if "disclaimer" not in st.session_state:
            with st.empty():
                for seconds in range(3):
                    st.warning(
                        "‎ You can click on 👍 or 👎 to provide feedback regarding the quality of responses.",
                        icon="💡",
                    )
                    time.sleep(1)
                st.write("")
                st.session_state["disclaimer"] = True

        else:

            pass

    if "last_prompt" in st.session_state:
        st.write(st.session_state["last_prompt"])

else:

    st.error("You have reached the demo maximum messages.")
