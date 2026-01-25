from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os


load_dotenv()

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)
search_tool = SerperDevTool()
topic = input("Enter a topic you want to learn about: ")

researcher_agent = Agent(
    role="Researcher",
    goal="Gather accurate and relevant information",
    backstory="You are an expert researcher skilled at finding trustworthy information.",
    llm=llm,
    tools=[search_tool]
)

planner_agent = Agent(
    role="Planner",
    goal="Organize research into a clear learning structure",
    backstory="You are great at breaking complex topics into easy steps.",
    llm=llm
)

writer_agent = Agent(
    role="Writer",
    goal="Explain the topic in simple and engaging language",
    backstory="You are a friendly teacher who explains things clearly.",
    llm=llm
)

editor_agent = Agent(
    role="Editor",
    goal="Improve clarity, grammar, and flow",
    backstory="You polish content to make it professional and easy to read.",
    llm=llm
)

reviewer_agent = Agent(
    role="Reviewer",
    goal="Check correctness and completeness",
    backstory="You ensure the final content is accurate and beginner-friendly.",
    llm=llm
)

research_task = Task(
    description=f"Research the topic: {topic} using online sources.",
    expected_output="Detailed research notes with facts and examples.",
    agent=researcher_agent
)

planning_task = Task(
    description="Create a structured outline based on the research.",
    expected_output="A clear step-by-step outline of the topic.",
    agent=planner_agent
)

writing_task = Task(
    description="Write an easy-to-understand explanation using the outline.",
    expected_output="A beginner-friendly explanation of the topic.",
    agent=writer_agent
)

editing_task = Task(
    description="Edit the content for clarity, grammar, and flow.",
    expected_output="Polished and well-written content.",
    agent=editor_agent
)

reviewing_task = Task(
    description="Review the final content for accuracy and completeness.",
    expected_output="Final approved version ready for learning.",
    agent=reviewer_agent
)

crew = Crew(
    agents=[researcher_agent,planner_agent,writer_agent,editor_agent,reviewer_agent],
    tasks=[research_task,planning_task,writing_task,editing_task,reviewing_task],
    verbose=False
)

result = crew.kickoff(inputs={"topic": topic})
print("FINAL OUTPUT:\n")
print(result)
