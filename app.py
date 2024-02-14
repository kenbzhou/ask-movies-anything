import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from model import prompt_client

st.set_page_config(page_title="Find out movie information from IMDB!", page_icon ="🎬")
st.title("Chat with IMDB")

if "history" not in st.session_state:
    st.session_state.history = [
        AIMessage(content="Ask me any question related to an existant movie!")
    ]

userInput = st.chat_input("Ask your question here...")
if userInput is not None and userInput != "":
    st.session_state.history.append(HumanMessage(content=userInput))
    with st.chat_message("You"):
        st.write(userInput)

    response = prompt_client(userInput)
    st.session_state.history.append(AIMessage(content=response))
    with st.chat_message("AI"):
        st.write(response)


#for message in st.session_state.history:
#    if isinstance(message, AIMessage):
#        with st.chat_message("AI"):
#            st.write(message.content)
#    elif isinstance(message, HumanMessage):
#        with st.chat_message("You"):
#            st.write(message.content)

