from tasks.celery_app import celery_app
from src.project_flow.crews.content_crew.content_crew import ContentCrew
from src.project_flow.crews.analisator.analisator import Analisator
from src.project_flow.crews.system_analyser.system_analyser import SystemAnalyser
from src.project_flow.crews.developer.developer import Developer
from src.project_flow.crews.file_analyzer.file_analyzer import FileAnalyzer
from src.project_flow.crews.excel_analyzer.excel_analyzer import ExcelAnalyzer
from src.project_flow.crews.json_analyzer.json_analyzer import JsonAnalyzer
from src.project_flow.crews.crew_anomali.crew_anomali import CrewAnomali
import logging
import traceback

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, name='research')
def research(self, topic: str):
    self.update_state(state='RUNNING', meta={'current':f"start job for: {topic}"})
    try:
        result = ContentCrew().crew().kickoff(inputs={"topic": topic})
        return str(result)
    except Exception as e:
        logger.error(f"Error in research task: {str(e)}")
        logger.error(traceback.format_exc())
        raise e
    
@celery_app.task(bind=True, name='market_research')
def market_research(self, topic: str, location: str, year: int):
    self.update_state(state='RUNNING', meta={'current':f"start job for: {topic}"})
    try:
        result = Analisator().crew().kickoff(inputs={"topic": topic, "location": location, "year": year})
        return str(result)
    except Exception as e:
        logger.error(f"Error in market research task: {str(e)}")
        logger.error(traceback.format_exc())
        raise e
    
@celery_app.task(bind=True, name='analyzing_task')
def analyzing_task(self, topic: str, style: str):
    self.update_state(state='RUNNING', meta={'current':f"start job for: {topic}"})
    try:
        result = SystemAnalyser().crew().kickoff(inputs={"topic": topic, "style": style})
        return str(result)
    except Exception as e:
        logger.error(f"Error in system analysis task: {str(e)}")
        logger.error(traceback.format_exc())
        raise e
    
@celery_app.task(bind=True, name='developer_task')
def developer_task(self, topic: str, language: str):
    self.update_state(state='RUNNING', meta={'current':f"start job for: {topic}"})
    try:
        result = Developer().crew().kickoff(inputs={"topic": topic, "language": language})
        return str(result)
    except Exception as e:
        logger.error(f"Error in developer task: {str(e)}")
        logger.error(traceback.format_exc())
        raise e
    
@celery_app.task(bind=True, name='file_analyzer_task')
def file_analyzer_task(self, file: str):
    self.update_state(state='RUNNING', meta={'current':f"start job for: {file}"})
    try:
        result = FileAnalyzer().crew().kickoff(inputs={"file": file})
        return result.json_dict
    except Exception as e:
        logger.error(f"Error in file analyzer task: {str(e)}")
        logger.error(traceback.format_exc())
        raise e
    
@celery_app.task(bind=True, name='excel_analyzer_task')
def excel_analyzer_task(self, file: str):
    self.update_state(state='RUNNING', meta={'current':f"start job for: {file}"})
    try:
        result = ExcelAnalyzer().crew().kickoff(inputs={"file": file})
        return result.json_dict
    except Exception as e:
        logger.error(f"Error in excel analyzer task: {str(e)}")
        logger.error(traceback.format_exc())
        raise e
    
@celery_app.task(bind=True, name='json_analyzer_task')
def json_analyzer_task(self, file: str):
    self.update_state(state='RUNNING', meta={'current':f"start job for: {file}"})
    try:
        result = JsonAnalyzer().crew().kickoff(inputs={"file": file})
        return result.json_dict
    except Exception as e:
        logger.error(f"Error in json analyzer task: {str(e)}")
        logger.error(traceback.format_exc())
        raise e
    
@celery_app.task(bind=True, name='deteksi_anomali_excel')
def deteksi_anomali_excel(self, file: str):
    self.update_state(state='RUNNING', meta={'current':f"start job for: {file}"})
    try:
        result = CrewAnomali().crew().kickoff(inputs={"file": file})
        return str(result)
    except Exception as e:
        logger.error(f"Error in anomaly detection task: {str(e)}")
        logger.error(traceback.format_exc())
        raise e