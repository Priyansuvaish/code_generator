import subprocess
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool,FileWriterTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
load_dotenv()

@CrewBase
class ModelLayer:
    

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = ChatOpenAI(model=os.getenv("MODEL"))

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def model_developer(self) -> Agent:
        if 'model_developer' not in self.agents_config:
            raise KeyError("Missing configuration for 'model_developer' in agents_config.")
        return Agent(
            config=self.agents_config['model_developer'],
            allow_delegation=True,
            verbose=True,
            llm="gpt-4o",
            tools=[FileWriterTool()],
            memory=False,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def generate_model_layer(self) -> Task:
        if 'generate_model_layer' not in self.tasks_config:
            raise KeyError("Missing configuration for 'generate_model_layer' in tasks_config.")
        return Task(
            config=self.tasks_config['generate_model_layer'],
            agent=self.model_developer()
        )

    # @task
    # def verify_application(self) -> Task:
    #     def verification_logic():
    #         try:
    #             project_dir = os.path.abspath(r"E:\code_generator\demo")
    #             if not os.path.exists(project_dir):
    #                 return f"Directory {project_dir} does not exist. Check the project path."

    #             # Compile the Spring Boot project
    #             build_command = ["mvn", "clean", "package"]
    #             build_process = subprocess.check_call(
    #                 build_command,
    #                 cwd=project_dir,
    #                 capture_output=True, text=True, check=True,shell=True
    #             )
    #             print("Build Output:", build_process.stdout)
    #             print("Build Errors:", build_process.stderr)
    #             if build_process.returncode != 0:
    #                 return f"Build failed: {build_process.stderr}"

    #             # Check if the jar file exists
    #             jar_file_path = os.path.join(project_dir, "target","", "app.jar")
    #             if not os.path.exists(jar_file_path):
    #                 return f"JAR file not found at {jar_file_path}. Check the build process."

    #             # Run the generated Spring Boot application
    #             run_process = subprocess.Popen(
    #                 ["java", "-jar", jar_file_path],
    #                 cwd=project_dir,
    #                 capture_output=True, text=True, check=True
    #             )
    #             print("Run Output:", run_process.stdout)
    #             return "Application ran successfully."

    #         except subprocess.CalledProcessError as e:
    #             error_message = f"Error during execution: {e.stderr or e.stdout}"
    #             print(error_message)
    #             return error_message

    #     return Task(
    #         agent=self.model_developer(),
    #         description="Verifies if the generated Spring Boot application is runnable.",
    #         expected_output="Application runs successfully without errors.",
    #         task_fn=verification_logic
    #     )


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
