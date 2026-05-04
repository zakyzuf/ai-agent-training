from tasks.celery_app import celery_app
from src.project_flow.crews.content_crew.content_crew import ContentCrew
from src.project_flow.crews.analisator.analisator import Analisator
from src.project_flow.crews.system_analyser.system_analyser import SystemAnalyser
from src.project_flow.crews.developer.developer import Developer
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