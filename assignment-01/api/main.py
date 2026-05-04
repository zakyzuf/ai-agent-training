from fastapi import FastAPI, UploadFile, BackgroundTasks, HTTPException, Response
import os
import uuid
from http import HTTPStatus
from pydantic import BaseModel
from tasks.celery_app import celery_app 
from tasks import celery_task as celeryTask
from celery.result import AsyncResult

class ResearchInput(BaseModel):
    topic: str
    
class MarketResearchInput(BaseModel):
    topic: str
    location: str
    year: int
    
class ResearchStatus(BaseModel):
    task_id: str
    status: str
    result: str = None
    error: str = None
    
class AnalyzingInput(BaseModel):
    topic: str
    style: str

class DeveloperInput(BaseModel):
    topic: str
    language: str

app = FastAPI()

@app.post("/tes")

async def tes():
    # Simulate tes process
    return {"message": "tes endpoint is under construction."}

@app.post("/research")
async def research(researchInput: ResearchInput):
    task = celery_task.research.delay(researchInput.topic)
    return {"task_id": task.id}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    
    response = {
        "task_id": task_id,
        "status": task_result.state,
        "result": None,
        "error": None
    }
    
    if task_result.state == 'SUCCESS':
        response["result"] = str(task_result.result)
    elif task_result.state == 'FAILURE':
        response["error"] = str(task_result.info)
        
    return response

@app.post("/market-research")
async def market_research(marketResearchInput: MarketResearchInput):
    task = celery_task.market_research.delay(
        marketResearchInput.topic,
        marketResearchInput.location,
        marketResearchInput.year
    )
    return {"task_id": task.id}

@app.post("/analyzing")
async def analyzing(analyzingInput: AnalyzingInput):
    task = celeryTask.analyzing_task.delay(analyzingInput.topic, analyzingInput.style)
    return {"task_id": task.id}

@app.post("/developer")
async def developer(developerInput: DeveloperInput):
    task = celeryTask.developer_task.delay(developerInput.topic, developerInput.language)
    return {"task_id": task.id}

@app.get("/get-status/{task_id}", response_model=ResearchStatus)
async def get_status2(task_id: str):
    task_result = celeryTask.celery_app.AsyncResult(task_id)
    if task_result.state == "PENDING":
        return ResearchStatus(task_id=task_id, status="PENDING")
    elif task_result.state == "RUNNING":
        return ResearchStatus(task_id=task_id, status="RUNNING")
    elif task_result.state == "SUCCESS":
        return ResearchStatus(task_id=task_id, status="SUCCESS", result=task_result.result)
    elif task_result.state == "FAILURE":
        return ResearchStatus(task_id=task_id, status="FAILURE", error=str(task_result.result))
    else:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Unknown task state")