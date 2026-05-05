from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileReadTool
from pydantic import BaseModel, Field
from src.project_flow.tools.excel_read_tool import ExcelReadTool


# Pindahkan Output model ke LUAR class
class Output_excel_analyzer(BaseModel):
    insight: str
    indicator: str
    
class Output_excel_analyzer_list(BaseModel):
    analyzer: list["Output_excel_analyzer"] = Field(..., min_length = 5)

@CrewBase
class ExcelAnalyzer():  # Fix typo: FileAnalyszer → FileAnalyzer
    """ExcelAnalyzer crew"""

    agents: list[BaseAgent]
    tasks: list[Task]
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # fileReadTool = FileReadTool()
    excelReadTool = ExcelReadTool()
    
    @agent
    def senior_excel_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_excel_analyzer'],  # type: ignore[index]
            verbose=True,
            tools=[self.excelReadTool]
        )

    @task
    def task_excel_analyzer(self) -> Task:
        return Task(
            config=self.tasks_config['task_excel_analyzer'],  # type: ignore[index]
            output_file='output/excel_analysis.md',
            output_excel=Output_excel_analyzer_list
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ExcelAnalyzer crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )