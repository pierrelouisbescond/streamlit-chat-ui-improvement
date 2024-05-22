
## 🤩 Streamlit Chat Improvement

This side project aims to add new functionalities to the standard [Streamlit chat interface](https://docs.streamlit.io/develop/api-reference/chat):

-   📥 Chat history export (in JSON format)
-   🧹 Clear chat
-   🔁 Rerun last question
-   👍 and 👎 feedback buttons (registered in the logs)
-   💬 tokens count
-   👩‍💻 chat avatars personalization

The video below shows how they integrate into the UI:

![Streamlit Chat Improved UI](./images/streamlit-chat-improvement-30.gif)


The logs corresponding to the feedback buttons are:

```
INFO:root:2024-05-22 14:35:23: positive: [{"role": "user", "content": "1+1"}, {"role": "assistant", "content": "1+1 equals 2."}]
INFO:root:2024-05-22 14:35:30: negative: [{"role": "user", "content": "2+2"}, {"role": "assistant", "content": "2 + 2 equals 4."}]
```

The demo hosted [here](https://chat-ui-improvement.streamlit.app/) is limited to 3 questions and/or 300 tokens.

The code does not leverage all possible improvements offered by Streamlit (like caching) so I look forward to getting pull requests to make this small project better 😁