import openai
import os
import streamlit as st
from dotenv import load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


# Load environment variables from .env file
load_dotenv()

# Set up your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Init LLM
llm = ChatOpenAI(temperature=0.5)



message = [
    SystemMessage(
        content="A user will input a question regarding various aspects of a movie, like its rating, main story line, main actors, etc."
    ),
    HumanMessage(
        content="What is the rating of the movie xyz?",
    ),
]

response = llm.invoke(message)
print(response)