from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import pandas as pd

class ExcelReadToolInput(BaseModel):
    file_path: str = Field(..., description="Path to the .xlsx file")

class ExcelReadTool(BaseTool):
    name: str = "Read Excel File"
    description: str = "Reads an .xlsx file and returns its content as a string"
    args_schema: type[BaseModel] = ExcelReadToolInput

    def _run(self, file_path: str) -> str:
        try:
            df = pd.read_excel(file_path)
            return df.to_string()
        except Exception as e:
            return f"Error reading Excel file: {e}"

xlsx_tool = ExcelReadTool()
