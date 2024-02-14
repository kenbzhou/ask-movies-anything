import os
import requests
import handler
from dotenv import load_dotenv
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, AgentType

def prompt_client(prompt):
    # Load environment variables from .env file
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Instantiate OpenAI and prompt template
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    prompt_template = "Output the desired attribute '{content}' from the returned data"
    llm_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(prompt_template)
    )

    # Instantiate tools
    handle_bad_prompt_tool = Tool.from_function(
        func=lambda x: "Politely tell them to provide a prompt relevant to a movie in IMDB's catalogue.",
        name="badPrompter",
        description="Handles a prompt unrelated to a movie."
    )

    prompt_template_ambig = "Try to find the movie title an ambiguous description: {content}"
    llm_ambig_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt_template_ambig))
    ambiguous_tool = Tool.from_function(
        func=llm_ambig_chain.run,
        name="Disambiguator",
        description="Given an ambiguous description of a movie, try to come up with its exact movie title."
    )


    check_if_movie_exists = Tool.from_function(
        func=handler.get_data_by_title,
        name="movieChecker",
        description="Check if a movie exists from the string of its title."
    )

    maturity_level_tool = Tool.from_function(
        func=handler.get_maturity_level,
        name="MaturityLevelGetter",
        description="Fetches the maturity level of a show/movie from the string of its title."
    )

    release_year_tool = Tool.from_function(
        func=handler.get_release_year,
        name="ReleaseYearGetter",
        description="Fetches the release year of a show/movie from the string of its title."
    )

    plot_tool = Tool.from_function(
        func=handler.get_plot,
        name="PlotGetter",
        description="Fetches the plot of a show/movie from the string of its title."
    )

    rating_tool = Tool.from_function(
        func=handler.get_rating,
        name="RatingGetter",
        description="Fetches the critical rating of a show/movie from the string of its title."
    )

    cast_tool = Tool.from_function(
        func=handler.get_cast,
        name="CastGetter",
        description="Fetches the cast/actors of a show/movie from the string of its title."
    )

    character_tool = Tool.from_function(
        func=handler.get_characters,
        name="CharacterGetter",
        description="Fetches the characters of a show/movie from the string of its title."
    )

    tools = [check_if_movie_exists, maturity_level_tool, release_year_tool, 
             plot_tool, rating_tool, cast_tool, character_tool, handle_bad_prompt_tool, ambiguous_tool]


    agent = initialize_agent(
        tools=tools,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        llm=llm,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent.invoke(prompt)['output']


