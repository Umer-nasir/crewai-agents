import streamlit as st
import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import ScrapeWebsiteTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="CrewAI Cold Email Generator",
    page_icon="📧",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1E3A8A;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #3B82F6;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2563EB;
    }
    .email-container {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .status-box {
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    .status-running {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        color: #1D4ED8;
    }
    .status-complete {
        background-color: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #047857;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>📧 CrewAI Cold Email Generator</h1>", unsafe_allow_html=True)
st.markdown("Generate personalized cold emails by analyzing company websites with AI agents")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your Gemini API Key", type="password", help="Get your API key from Google AI Studio")

    if api_key:
        st.success("✅ API Key configured")
    else:
        st.warning("⚠️ Please provide an API Key to run the crew")
        # Stop execution if no key is provided, but allow viewing the UI
    
    st.markdown("---")
    st.subheader("How it works:")
    st.markdown("""
    1. **Researcher**: Analyzes company website
    2. **Strategist**: Matches needs with services
    3. **Writer**: Crafts personalized email
    """)
    
    st.markdown("---")
    st.subheader("Agency Services:")
    st.markdown("""
    1. Content Related Ads
    2. Neutral Visions
    3. AI Automation
    """)

# Main input area
st.markdown("### Enter Target Company URL")
url = st.text_input(
    "Website URL", 
    placeholder="https://example.com",
    help="Enter the URL of the company you want to research"
)

# Agency services (same as in your business.py)
agency_services = """
1. Content Related Ads: Best for websites who have good content but ugly ads. We provide best adds for your website.
2. Neutral visions for visually overwhelming, hard to look at, or dull/boring websites: Best for websites who have dull colors or very bright colors that affects eyes of visitors or another they do not admire the visitors. Our website provide best vision for the visitors eye that will make them to admire the website.
3. AI Automation: Best for companies with manual, repetitive tasks. We build agents to save time.
"""

# Initialize session state
if 'result' not in st.session_state:
    st.session_state.result = None
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# Generate button
col1, col2 = st.columns([1, 1])
with col1:
    generate_btn = st.button("🚀 Generate Cold Email", disabled=st.session_state.is_running or not url or not api_key, type="primary")
with col2:
    clear_btn = st.button("🗑️ Clear Results")

if clear_btn:
    st.session_state.result = None
    st.session_state.is_running = False
    st.rerun()

# Main processing logic
if generate_btn and url and api_key:
    st.session_state.is_running = True
    st.session_state.result = None
    
    try:
        # Status indicator
        status_placeholder = st.empty()
        status_placeholder.markdown(
            '<div class="status-box status-running">🤖 Researcher is analyzing the website...</div>', 
            unsafe_allow_html=True
        )
        
        # Initialize LLM
        llm = LLM(
            model="gemini/gemini-2.5-flash",
            api_key=api_key
        )
        
        # Create scraping tool with dynamic URL
        scrape_tool = ScrapeWebsiteTool(url=url)
        
        # Create agents (same as your original code)
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
        
        # Update status
        status_placeholder.markdown(
            '<div class="status-box status-running">🧠 Strategist is matching services...</div>', 
            unsafe_allow_html=True
        )
        
        # Create tasks (with dynamic URL)
        task_analyze = Task(
            description=f"Scrape the website {url}. Summarize what the company does and identify 1 key area where they could improve (e.g., design, traffic, automation).",
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
        
        # Update status
        status_placeholder.markdown(
            '<div class="status-box status-running">✍️ Writer is crafting the email...</div>', 
            unsafe_allow_html=True
        )
        
        # Create and run crew (same as your original code)
        sales_crew = Crew(
            agents=[researcher, strategist, writer],
            tasks=[task_analyze, task_strategize, task_write],
            process=Process.sequential,
            verbose=False,
            llm=llm
        )
        
        # Run the crew
        result = sales_crew.kickoff()
        
        # Store result and update status
        st.session_state.result = result
        st.session_state.is_running = False
        status_placeholder.markdown(
            '<div class="status-box status-complete">✅ Email generated successfully!</div>', 
            unsafe_allow_html=True
        )
        
    except Exception as e:
        st.session_state.is_running = False
        status_placeholder.empty()
        st.error(f"❌ Error: {str(e)}")
        st.info("Make sure your API key is correct and the website is accessible.")

# Display results
if st.session_state.result:
    st.markdown("---")
    st.subheader("📧 Generated Cold Email")
    
    # Convert result to string to handle CrewOutput object
    result_str = str(st.session_state.result)
    
    # Display the email in a nice container
    st.markdown(
        f"""
        <div class="email-container">
            <h4>To: CEO of Target Company</h4>
            <h4>Subject: Quick question about your website</h4>
            <p>{result_str}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Copy button
    st.download_button(
        label="📋 Copy Email Text",
        data=result_str,
        file_name="cold_email.txt",
        mime="text/plain"
    )
    
    # Word count
    word_count = len(result_str.split())
    st.caption(f"Word count: {word_count}/150")

# Footer
st.markdown("---")
st.caption("Powered by CrewAI and Streamlit | Keep your emails under 150 words for best results")
