import os
import requests
from imdb_handler import get_imdb_data_by_title
from dotenv import load_dotenv
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, AgentType

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

movie_data_extraction_tool = Tool.from_function(
    func=get_imdb_data_by_title,
    name="DataFetcher",
    description="Fetches movie or show data from the string of its title into a json"
)

prompt_template = "Output the desired attribute of {content}"
llm = ChatOpenAI(model="gpt-3.5-turbo")
llm_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(prompt_template)
)

outputter_tool = Tool.from_function(
    func=llm_chain.run,
    name="Outputter",
    description="Outputs the desired attribute from a jsonified list of attributes"
)

tools = [movie_data_extraction_tool, outputter_tool]

agent = initialize_agent(
    tools=tools,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    llm=llm,
    verbose=True
)

prompt = "What is the cast of The Office?"
print(agent.invoke(prompt))




# initialize the models


# Step 1: User Provides Input

# Step 2: Input is parsed into a movie or show title.

# Step 3: Movie/Show Title is passed into the IMDB API

# Step 4: IMDB JSON is provided as context for a final response.
