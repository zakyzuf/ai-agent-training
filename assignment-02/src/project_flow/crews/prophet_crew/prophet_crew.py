from pydantic import BaseModel, Field
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.project_flow.tools.prophet_tool import ProphetTool


class Output_prophet_analyzer(BaseModel):
    insight: str = Field(description="Business explanation or narrative based on the temperature prediction results.")
    indicator: str = Field(description="The relevant metric or number (e.g., Average 890°C, Max 905°C).")

class Output_prophet_analyzer_list(BaseModel):
    analyzer: list["Output_prophet_analyzer"] = Field(..., min_length=5)

@CrewBase
class ProphetAnalyzer():
    """ProphetAnalyzer crew for Predictive Maintenance"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def senior_data_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_data_analyzer'],
            verbose=True,
            tools=[ProphetTool()] # Inject the custom tool here
        )

    @task
    def task_data_analyzer(self) -> Task:
        return Task(
            config=self.tasks_config['task_data_analyzer'],
            output_file='output/prophet_analysis.json', # You can change this to .md if preferred
            output_pydantic=Output_prophet_analyzer_list # Enforce Pydantic output
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.senior_data_analyzer()],
            tasks=[self.task_data_analyzer()],
            process=Process.sequential,
            verbose=True,
        )