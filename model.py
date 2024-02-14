import openai
import os
import streamlit as st
from dotenv import load_dotenv
from langchain import LLMContext, LLMChain, OpenAI
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain.schema import HumanMessage, SystemMessage


# Load environment variables from .env file
load_dotenv()

# Set up your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Init LLM
llm = ChatOpenAI(temperature=0.5)

message = [
    SystemMessage(
        content="A user will input an actor and you will output their top grossing movie"
    ),
    HumanMessage(
        content="Brad Pitt"
    ),
]

response = llm.invoke(message)
print(response)
