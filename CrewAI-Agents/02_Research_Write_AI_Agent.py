# QA Research Analyst
# QA Documentation Writer


# Fix SSL cert verification on Windows: uv's Python looks for CA certs at a
# non-existent Unix path. Must be set BEFORE importing ssl/httpx (via crewai),
# otherwise Python's ssl module never sees it.
import os
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()

from crewai import Agent, Task, Crew, Process
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

openrouter_llm = LLM(
    model=os.getenv("OPENROUTER_MODEL", "openrouter/deepseek/deepseek-v4-flash"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("BASE_URL", "https://openrouter.ai/api/v1"),
)

researcher_agent = Agent(
        role="QA Research Analyst",
        goal = "Find the common bugs in the web application",
        backstory="You are a QA researcher who has analyzed " \
        "thousands of bug reports across web applications. " \
        "You specialize in identifying patterns and trends in software defects.",
        llm=openrouter_llm,
        verbose=True
)

writer_agent = Agent(
    role="QA Documentation Writer",
    goal="Create clear, actionable bug prevention guidelines",
    backstory="""You are a technical writer specializing in QA 
    documentation. You turn complex bug data into simple, 
    actionable checklists that developers can follow.""",
    llm=openrouter_llm,
    verbose=True
)

researcher_task = Task(
    description="""Research and list the top 5 most common bug 
    categories in modern web applications. For each category, 
    provide: name, frequency (percentage), example, and impact level.""",
    expected_output="""A ranked list of 5 bug categories with 
    name, frequency, example, and impact for each.""",
    agent=researcher_agent
)

writing_task = Task(
    description="""Based on the research provided, create a 
    'Bug Prevention Checklist' that developers can use before 
    submitting a pull request. Make it practical and actionable.""",
    expected_output="""A formatted checklist with 5-10 items 
    that developers can quickly review before code submission.""",
    agent=writer_agent
)

crew = Crew(
    agents= [researcher_agent,writer_agent],
    tasks=[researcher_task,writing_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
print(result)