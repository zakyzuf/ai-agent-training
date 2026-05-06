import json
# from unittest import result

from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException, Response
import os
import uuid
from http import HTTPStatus
from pydantic import BaseModel
from tasks.celery_app import celery_app 
from tasks import celery_task as celeryTask
from celery.result import AsyncResult

TEXT_FOLDER = "files_test"
EXCEL_FOLDER = "files_excel"
JSON_FOLDER = "files_json"
os.makedirs(TEXT_FOLDER, exist_ok=True)
os.makedirs(EXCEL_FOLDER, exist_ok=True)
os.makedirs(JSON_FOLDER, exist_ok=True)

class ResearchInput(BaseModel):
    topic: str
    
class MarketResearchInput(BaseModel):
    topic: str
    location: str
    year: int
    
class ResearchStatus(BaseModel):
    task_id: str
    status: str
    result: dict | str | None = None
    error: str | None = None
    
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
        if isinstance(task_result.result, str):
            try:
                result = json.loads(task_result.result)
            except Exception as e:
                result = task_result.result
        else:
            result = task_result.result
        return ResearchStatus(task_id=task_id, status="SUCCESS", result=task_result.result)
    elif task_result.state == "FAILURE":
        return ResearchStatus(task_id=task_id, status="FAILURE", error=str(task_result.result))
    else:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Unknown task state")
    
@app.post("/file-analyzer")
async def file_analyzer(file: UploadFile):
    if file.content_type != 'text/plain':
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Only text files are allowed.")
    
    _, file_extension = os.path.splitext(file.filename or "file")
    file_extension = file_extension or ".txt"
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(TEXT_FOLDER, unique_filename)
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    task = celeryTask.file_analyzer_task.delay(file_path)
    return {"task_id": task.id, "file_path": file_path}

@app.post("/excel-analyzer")
async def excel_analyzer(file: UploadFile):
    if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Only Excel files are allowed.")
    
    _, file_extension = os.path.splitext(file.filename or "file")
    file_extension = file_extension or ".xlsx"
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(EXCEL_FOLDER, unique_filename)
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    task = celeryTask.excel_analyzer_task.delay(file_path)
    return {"task_id": task.id, "file_path": file_path}

@app.post("/json-analyzer")
async def json_analyzer(file: UploadFile):
    if file.content_type != 'application/json':
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Only JSON files are allowed.")
    
    _, file_extension = os.path.splitext(file.filename or "file")
    file_extension = file_extension or ".json"
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(JSON_FOLDER, unique_filename)
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    task = celeryTask.json_analyzer_task.delay(file_path)
    return {"task_id": task.id, "file_path": file_path}

@app.post("/deteksi-anomali-excel")
async def deteksi_anomali_excel(file: UploadFile):
    if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Only Excel files are allowed.")
    _, file_extension = os.path.splitext(file.filename or "file")
    file_extension = file_extension or ".xlsx"
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(TEXT_FOLDER, unique_filename)
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    task = celeryTask.deteksi_anomali_excel.delay(file_path)
    return {"task_id": task.id, "file_path": file_path}

@app.post("/prophet-analyzer")
async def prophet_analyzer(file: UploadFile = File(...)): 
    
    if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Only Excel files are allowed.")
    
    _, file_extension = os.path.splitext(file.filename or "file")
    file_extension = file_extension or ".xlsx"
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(EXCEL_FOLDER, unique_filename)
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    task = celeryTask.prophet_analyzer_task.delay(file_path)
    return {"task_id": task.id, "file_path": file_path}

@app.get("/get-status-prophet/{task_id}", response_model=ResearchStatus)
async def get_status_prophet(task_id: str):
    task_result = celeryTask.celery_app.AsyncResult(task_id)
    if task_result.state == "PENDING":
        return ResearchStatus(task_id=task_id, status="PENDING")
    elif task_result.state == "RUNNING":
        return ResearchStatus(task_id=task_id, status="RUNNING")
    elif task_result.state == "SUCCESS":
        if isinstance(task_result.result, str):
            try:
                result = json.loads(task_result.result)
            except Exception as e:
                result = task_result.result
        else:
            result = task_result.result

        return ResearchStatus(task_id=task_id, status="SUCCESS", result=result)
        
    elif task_result.state == "FAILURE":
        return ResearchStatus(task_id=task_id, status="FAILURE", error=str(task_result.result))
    else:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Unknown task state")