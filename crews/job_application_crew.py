# This file coordinates your AI agents
# Each agent has a specific role in the job application process

import os
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq

class JobApplicationSystem:
    def __init__(self):
        # Initialize Groq (FREE AI MODEL)
        # Groq gives you fast, free access to Llama models
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-70b-versatile"  # This is FREE!
        )

    def create_job_scout_agent(self):
        """This agent finds relevant jobs"""
        return Agent(
            role="Job Scout",
            goal="Find jobs matching my skills",
            backstory="I'm an expert at finding hidden job opportunities",
            llm=self.llm,
            verbose=True  # Shows what the agent is thinking
        )

    def create_analyzer_agent(self):
        """This agent scores how well you match each job"""
        return Agent(
            role="Job Analyzer",
            goal="Score job compatibility from 1-10",
            backstory="I analyze job requirements against resumes",
            llm=self.llm,
            verbose=True
        )

    def create_resume_writer_agent(self):
        """This agent customizes resumes for specific jobs"""
        return Agent(
            role="Resume Writer",
            goal="Create tailored resumes for each job application",
            backstory="I specialize in crafting compelling resumes that highlight relevant skills and experience for specific job requirements",
            llm=self.llm,
            verbose=True
        )

    def analyze_job_compatibility(self, job_description, user_resume):
        """Analyze how well a job matches the user's profile"""
        analyzer = self.create_analyzer_agent()

        task = Task(
            description=f"""
            Analyze the job compatibility between the job description and resume:

            Job Description:
            {job_description}

            User Resume:
            {user_resume}

            Provide a compatibility score from 1-10 and list matching skills.
            """,
            expected_output="A compatibility score (1-10) and detailed analysis of matching skills and requirements",
            agent=analyzer
        )

        crew = Crew(
            agents=[analyzer],
            tasks=[task],
            verbose=True
        )

        return crew.kickoff()

    def generate_tailored_resume(self, job_description, base_resume):
        """Generate a tailored resume for a specific job"""
        resume_writer = self.create_resume_writer_agent()

        task = Task(
            description=f"""
            Create a tailored resume based on the job requirements:

            Job Description:
            {job_description}

            Base Resume:
            {base_resume}

            Customize the resume to highlight relevant skills and experience.
            """,
            expected_output="A tailored resume emphasizing relevant skills and experience for the specific job",
            agent=resume_writer
        )

        crew = Crew(
            agents=[resume_writer],
            tasks=[task],
            verbose=True
        )

        return crew.kickoff()