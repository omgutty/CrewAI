# Fix SSL cert verification on Windows: uv's Python looks for CA certs at a
# non-existent Unix path. Must be set BEFORE importing ssl/httpx (via crewai),
# otherwise Python's ssl module never sees it.
import os
import certifi

#os.environ["SSL_CERT_FILE"] = certifi.where()

from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv


#By default Creq AI actuall the brain which user Open AI , we are using groq


# Step 0 - Set up the Brain
# Step 1. - Define the Agent (identity)
# Step 2. - Give the Task to the Agent
# Step 3. Add them to the Crew
# Step 4. Kick Off Agent.


# Step 0 - Load environment variables and set up the Groq LLM
load_dotenv()

openrouter_llm = LLM(
    model=os.getenv("OPENROUTER_MODEL", "openrouter/deepseek/deepseek-v4-flash"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("BASE_URL", "https://openrouter.ai/api/v1"),
) 

# Step 1. - Define the Agent (identity)
qa_agent= Agent(
    role= "QA Engineer",
    goal="Analyse the feature or the requirements, and create 5-10 test cases out of it.",
    backstory="You are a senior QA engineer with 15 years of experience in test planning and testcases creation",
    llm = openrouter_llm,
    verbose=True
)

# Step 2 - Give the Task to the Agent
test_case_task= Task(
    description="Create 5-10 test cases",
    expected_output="A numbered list of 5-10 test cases with brief descriptions for a https://www.saucedemo.com/ Login page with the username, password and Login button  functionality",
    agent=qa_agent
)

# Step 3. Add them to the Crew
crew=Crew(
    agents=[qa_agent],
    tasks=[test_case_task],
    verbose= True
)


# # Step 4. kickOff
# result = crew.kickoff()
# print(result)

# # Step 4. kickOff
# def test_agent():
#     result = crew.kickoff()
#     print(result)
#     assert result is not None

if __name__ == "__main__":
    result = crew.kickoff()
    print(result)