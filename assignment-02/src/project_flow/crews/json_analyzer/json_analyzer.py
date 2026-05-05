from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileReadTool
from pydantic import BaseModel, Field


# Pindahkan Output model ke LUAR class
class Output_json_analyzer(BaseModel):
    insight: str
    indicator: str
    
class Output_json_analyzer_list(BaseModel):
    analyzer: list["Output_json_analyzer"] = Field(..., min_length = 5)

@CrewBase
class JsonAnalyzer():  # Fix typo: FileAnalyszer → FileAnalyzer
    """JsonAnalyzer crew"""

    agents: list[BaseAgent]
    tasks: list[Task]
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    fileReadTool = FileReadTool()

    @agent
    def senior_json_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_json_analyzer'],  # type: ignore[index]
            verbose=True,
            tools=[self.fileReadTool]
        )

    @task
    def task_json_analyzer(self) -> Task:
        return Task(
            config=self.tasks_config['task_json_analyzer'],  # type: ignore[index]
            output_file='output/json_analysis.md',
            output_json=Output_json_analyzer_list
        )

    @crew
    def crew(self) -> Crew:
        """Creates the JsonAnalyzer crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )