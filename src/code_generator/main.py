#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from code_generator.crews.api_parser.api_parser import ApiParser
from code_generator.crews.Model_Layer.Model_Layer import ModelLayer
import requests
import zipfile
import os
import openai

# Load API key from environment variable
openai.api_key = os.getenv("OPEN_API_KEY")


class PoemState(BaseModel):
    project_name: str = ""
    package_name: str = ""
    dependencies: str = ""
    java_version: int = 11
    language: str = ""
    build_type:str='maven'
    boot_version:str='3.3.0'
    base_url:str = "https://start.spring.io/starter.zip"
    api_result: dict = {}
    entity_result: dict = {}
    
    


class PoemFlow(Flow[PoemState]):

    @start()
    def Intialization(self):
        print("Provide the details")
        self.state.project_name = input("Enter the project name: ")
        self.state.package_name = input("Enter the package name (e.g., com.example): ")
        self.state.dependencies = input("Enter the dependencies (comma separated, e.g., web,jpa): ").split(',')
        self.state.java_version = input("Enter Java version (default 11): ") or '11'
        self.state.language = input("Enter language (java/kotlin, default java): ") or 'java'

    @listen(Intialization)
    def generate_spring_boot_project(self):
        params = {
            'type': f'{self.state.build_type}-project',
            'language': self.state.language,
            'javaVersion': self.state.java_version,
            'dependencies': ','.join(self.state.dependencies),
            'artifactId': self.state.project_name,
            'groupId': self.state.package_name,
            'bootVersion': self.state.boot_version
        }

        print(params)
        response = requests.get(self.state.base_url, params=params)
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.text)

        if response.status_code == 200:
            zip_file_path = f'{self.state.project_name}.zip'
            with open(f'{self.state.project_name}.zip', 'wb') as file:
                file.write(response.content)
            if not os.path.exists(self.state.project_name):
                os.makedirs(self.state.project_name)

            # Unzip the file into the specified folder
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(self.state.project_name)
            
            # Remove the original ZIP file after extracting
            os.remove(zip_file_path)
            print(f"Unzipped the project to: {self.state.project_name}")
            return f"Spring Boot project {self.state.project_name} created successfully!"
        else:
            return "Failed"
        

    @listen(generate_spring_boot_project)
    def configure_application_properties(self):
        properties_content = """spring.datasource.url=jdbc:h2:mem:testdb
                                spring.datasource.driverClassName=org.h2.Driver
                                spring.datasource.username=sa
                                spring.datasource.password=password
                                spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
                                spring.h2.console.enabled=true
                                """

        properties_file_path = os.path.join(self.state.project_name, "src", "main", "resources", "application.properties")

        if not os.path.exists(os.path.dirname(properties_file_path)):
            os.makedirs(os.path.dirname(properties_file_path))

        with open(properties_file_path, 'w') as file:
            file.write(properties_content)

        print(f"application.properties configured successfully at {properties_file_path}")


    @listen(configure_application_properties)
    def api_parser(self):
        print("parsing the api")
        result = (
            ApiParser()
            .crew()
            .kickoff()
        )

        print("api result: ", result.raw)
        self.state.api_result = result.raw  # Save the result in state
        print("API parsed successfully and stored in state.")
    
    @listen(api_parser)
    def generate_model(self):
        print("Generating model")
        print("API Result: ", self.state.api_result)
        result = (
            ModelLayer()
            .crew()
            .kickoff(inputs={
                'api_result': self.state.api_result,
                'project_name': self.state.project_name,
                'package_name': self.state.package_name,
            })
        )
        print("Model result: ", result.raw)
        self.state.entity_result = result.raw  # Save the result in state
        print("Entity Model successfully and stored in state.")

def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
