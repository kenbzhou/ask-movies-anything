import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
import re
from model import prompt_client

def contains_image_url(text):
    url_regex = r'https?://\S+'
    image_extensions_regex = r'\.(jpg|jpeg|png|gif|bmp|svg)$'

    # Find all URLs in the text
    urls = re.findall(url_regex, text)
    print(urls)
    for url in urls:
        if re.search(image_extensions_regex, url, re.IGNORECASE):
            return True, urls
    return False, None

def render_messages():
    for message in st.session_state.history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                contains, url = contains_image_url(message.content)
                if contains:
                    st.image(url)
                else:
                    st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("You"):
                st.write(message.content)

st.set_page_config(page_title="Find out movie information from IMDB!", page_icon ="🎬")
st.title("Chat with IMDB")

if "history" not in st.session_state:
    st.session_state.history = [
        AIMessage(content="Ask me any question related to an existant movie or show!")
    ]

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

userInput = st.chat_input("Ask your question here...")
if userInput is not None and userInput != "":
    st.session_state.history.append(HumanMessage(content=userInput))
    response = prompt_client(userInput, st.session_state.memory)
    st.session_state.history.append(AIMessage(content=response))
    st.session_state.memory.save_context({"input": userInput}, {"output": response})


render_messages()


