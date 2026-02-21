import os
from crewai import Agent, Task, Crew, Process,LLM
from crewai_tools import ScrapeWebsiteTool
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

agency_services = """
1. Ad Optimization & Monetization: Best for websites who have good content but ugly ads. We provide best adds for your website.
2. UI/UX Redesign (Visual Optimization): Best for websites who have dull colors or very bright colors that affects eyes of visitors or another they do not admire the visitors.Our website provide best vision for the visitors eye that will make them to admire the website.
3. AI Automation & Workflow Systems: Best for companies with manual, repetitive tasks. We build agents to save time.
"""

scrape_tool = ScrapeWebsiteTool(url="https://www.berkshirehathaway.com/")

researcher = Agent(
    role='Business Intelligence Analyst',
    goal='Analyze the target company website and identify their core business and potential weaknesses.',
    backstory="You are an expert at analyzing businesses just by looking at their landing page. You look for what they do and where they might be struggling.",
    tools=[scrape_tool],
    verbose=False,
    allow_delegation=True,
    memory=True,
    llm=llm
)

strategist = Agent(
    role='Agency Strategist',
    goal='Match the target company needs with ONE of our agency services.',
    backstory=f"""You work for a top-tier digital agency.
    Your goal is to read the analysis of a prospect and decide which of OUR services to pitch.

    OUR SERVICES KNOWLEDGE BASE:
    {agency_services}

    You must pick the SINGLE best service for this specific client and explain why.""",
    verbose=False,
    memory=True,
    llm=llm
)

writer = Agent(
    role='Senior Sales Copywriter',
    goal='Write a personalized cold email that sounds human and professional and remove jerks.',
    backstory="""You write emails that get replies. You never sound robotic.
    You mention specific details found by the Researcher to prove we actually looked at their site.""",
    verbose=False,
    llm=llm,
)

target_url = "https://www.berkshirehathaway.com/"

task_analyze = Task(
    description=f"Scrape the website {target_url}. Summarize what the company does and identify 1 key area where they could improve (e.g., design, traffic, automation).",
    expected_output="A brief summary of the company and their potential pain points.",
    agent=researcher
)

task_strategize = Task(
    description="Based on the analysis, pick ONE service from our Agency Knowledge Base that solves their problem. Explain the match.",
    expected_output="The selected service and the reasoning for the match.",
    agent=strategist
)

task_write = Task(
    description="Draft a cold email to the CEO of the target company. Pitch the selected service. Keep it under 150 words.",
    expected_output="A professional cold email ready to send and jerks free.",
    agent=writer
)

sales_crew = Crew(
    agents=[researcher, strategist, writer],
    tasks=[task_analyze, task_strategize, task_write],
    process=Process.sequential,
    verbose=False,
    llm=llm
)

print("### STARTING SALES RESEARCH AGENT ###")
result = sales_crew.kickoff()

print("\n\n########################")
print("## FINAL EMAIL DRAFT ##")
print("########################\n")
print(result)