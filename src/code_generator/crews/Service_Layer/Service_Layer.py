from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool,FileWriterTool,DirectoryReadTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

from pydantic import BaseModel
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
load_dotenv()
# class ServiceLayerdata(BaseModel):
#     folder_path:str=""
#     project_name: str = ""
#     api_result: dict = {}
#     package_name: str = ""



@CrewBase
class ServiceLayer():
    

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = ChatOpenAI(model=os.getenv("MODEL"))

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    def __init__(self,folder_path:str):
        self.folder_path=folder_path
    @agent
    def service_developer(self) -> Agent:
        if 'service_developer' not in self.agents_config:
            raise KeyError("Missing configuration for 'service_developer' in agents_config.")
        print("folder_path for service 231",self.folder_path)
        return Agent(
            config=self.agents_config['service_developer'],
            allow_delegation=True,
            verbose=True,
            llm="gpt-4o",
            tools=[FileWriterTool(),DirectoryReadTool(directory=self.folder_path)],
            memory=False
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def generate_service_layer(self) -> Task:
        if 'generate_service_layer' not in self.tasks_config:
            raise KeyError("Missing configuration for 'generate_service_layer' in tasks_config.")
        return Task(
            config=self.tasks_config['generate_service_layer'],
            agent=self.service_developer()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
