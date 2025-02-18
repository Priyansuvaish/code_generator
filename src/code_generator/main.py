#!/usr/bin/env python
from random import randint

from pydantic import BaseModel
from typing import Optional
from crewai.flow.flow import Flow, listen, start, router, or_

from code_generator.crews.Api_Parser_Evaluator.api_parser_evaluator import ApiParserEvaluator
from code_generator.crews.Controller_Layer.Controller_Layer import ControllerLayer
from code_generator.crews.QA_Testing.QA_Testing import QaTester
from code_generator.crews.Service_Layer.Service_Layer import ServiceLayer
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
    folder_path: str = ""
    service_result: dict = {}
    controller_result: dict = {}
    count: int = 0
    flag: int =0
    feedback:Optional[str]=None
    Pass:bool=False
    
    


class PoemFlow(Flow[PoemState]):

    #We are taking the input from the user and creating a spring boot project
    @start()
    def Intialization(self):
        print("Provide the details")
        self.state.project_name = input("Enter the project name: ")
        self.state.package_name = input("Enter the package name (e.g., com.example): ")
        self.state.dependencies = input("Enter the dependencies (comma separated, e.g., web,jpa): ").split(',')
        self.state.java_version = input("Enter Java version (default 11): ") or '11'
        self.state.language = input("Enter language (java/kotlin, default java): ") or 'java'

    

    #We are creating a spring boot project using the details provided by the user
    @listen(or_(Intialization,"Failed"))
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
        

    #creating the application.properties file
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





    #We are parsing the api and storing the result in the state
    @listen(or_("Unsuccessful",configure_application_properties))
    def api_parser(self):
        print("parsing the api")
        result = (
            ApiParser()
            .crew()
            .kickoff()
        )

        # print("api result: ", result.raw)
        self.state.api_result = result.raw  # Save the result in state
        file_path = "api_result.md"

        # Write the API result to the file
        with open(file_path, "w") as file:
            file.write(f"api result: {self.state.api_result}\n")

        print(f"API result written to {file_path}")
        print("API parsed successfully and stored in state.")



    #We are evaluating the api parser result and if it is successful we are generating the model layer
    #If the api parser result is unsuccessful we are again parsing the api
    @router(api_parser)
    def evaluate_api_parser(self):
        print("Evaluating the API parser result")
        if(self.state.count>3):
            return "Successful"
        self.state.count += 1
        # print("API Result: ", self.state.api_result)
        result = (
            ApiParserEvaluator()
            .crew()
            .kickoff(inputs={'api_result': self.state.api_result})
        )
        file_path = "api_result_1.md"

        # Write the API result to the file
        with open(file_path, "w") as file:
            file.write(f"api 1 result: {result.raw}\n")

        if result.raw == "Successful":
            return "Successful"
        return "Unsuccessful"

        
        
    
    #If the api parser result is successful we are generating the model layer
    @listen("Successful")
    def generate_model(self):
        print("Generating model layer")
        print("API Result: ", self.state.api_result)
        # Example base path
        base_path = os.path.join(self.state.project_name, "src", "main", "java")
        # Convert package name to directory path
        package_path = self.state.package_name.replace('.', os.sep)
        # Full path to the models directory
        folder_path = os.path.join(base_path, package_path, self.state.project_name)
        self.state.folder_path = folder_path
        print(f"Entity directory path: {folder_path}")
        result = (
            ModelLayer()
            .crew()
            .kickoff(inputs={
                'api_result': self.state.api_result,
                'project_name': self.state.project_name,
                'package_name': self.state.package_name,
                'folder_path': folder_path
            })
        )
        # print("Model result: ", result.raw)
        self.state.entity_result = result.raw  # Save the result in state
        print("Entity_layer successfully and stored in state.")

    

    #We are generating the service layer
    @listen(generate_model)
    def generate_service(self):
        print("Generating service layer")
        result = (
            ServiceLayer()
            .crew()
            .kickoff(inputs={
                'api_result': self.state.api_result,
                'project_name': self.state.project_name,
                'package_name': self.state.package_name,
                'folder_path': self.state.folder_path
            })
        )
        # print("Model result: ", result.raw)
        self.state.service_result = result.raw  # Save the result in state
        print("Service_Layer successfully and stored in state.")



    #We are generating the controller layer
    @listen(generate_service)
    def generate_controller(self):
        print("Generating controller layer")
        result = (
            ControllerLayer()
            .crew()
            .kickoff(inputs={
                'api_result': self.state.api_result,
                'project_name': self.state.project_name,
                'package_name': self.state.package_name,
                'folder_path': self.state.folder_path
            })
        )
        # print("Controller result: ", result.raw)
        self.state.controller_result = result.raw  # Save the result in state
        print("Controller_Layer successfully and stored in state.")

    @router(generate_controller)
    def QaTesting(self):
        print("QA Testing")
     
        if(self.state.flag>3):
            return "Done"
        self.state.flag += 1
        # print("API Result: ", self.state.api_result)
        result = (
            QaTester()
            .crew()
            .kickoff()
        )
        file_path = "final_result.md"
        self.state.Pass=result["Pass"]
        self.state.feedback=result["feedback"]

        # Write the API result to the file
        with open(file_path, "w") as file:
            file.write(f"final result: {self.state.feedback}\n")

        if self.state.Pass == "True":
            return "Passed"
        return "Failed"
    
    @listen("Done")
    def done(self):
        print("Project Failed to create")
        print("Please try again")

        
    @listen("Passed")
    def final(self):
        print("Project is successfully created and tested")
       
    
        

        


def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
