from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
load_dotenv()

@CrewBase
class ApiParserEvaluator:
    

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = ChatOpenAI(model=os.getenv("MODEL"))

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def api_parser_evaluator(self) -> Agent:
        if 'api_parser_evaluator' not in self.agents_config:
            raise KeyError("Missing configuration for 'api_parser_evaluator' in agents_config.")
        return Agent(
            config=self.agents_config['api_parser_evaluator'],
            allow_delegation=True,
            verbose=True,
            llm="gpt-4o",
            tools=[FileReadTool(file_path=os.getenv('API_CONTRACT_PATH'))],
            memory=False
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def evaluate_api_parser_result(self) -> Task:
        if 'evaluate_api_parser_result' not in self.tasks_config:
            raise KeyError("Missing configuration for 'evaluate_api_parser_result' in tasks_config.")
        return Task(
            config=self.tasks_config['evaluate_api_parser_result'],
            agent=self.api_parser_evaluator()
        )

    @crew
    def crew(self) -> Crew:
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
