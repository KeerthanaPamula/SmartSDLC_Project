from fastapi import FastAPI, Request, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from app import logic

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

PROJECT_TITLE = "SmartSDLC – AI-Enhanced Software Development Lifecycle"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": PROJECT_TITLE
    })

@app.post("/analyze")
async def analyze(request: Request, prompt: str = Form(...), file: UploadFile = None):
    pdf_path = None
    if file:
        pdf_path = f"temp_{file.filename}"
        with open(pdf_path, "wb") as f:
            f.write(await file.read())
    result = logic.analyze_requirements(prompt, pdf_path)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result,
        "title": PROJECT_TITLE
    })

@app.post("/generate-code")
async def generate_code(request: Request, requirements: str = Form(...), language: str = Form(...), framework: str = Form(...)):
    result = logic.generate_code(requirements, language, framework)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result,
        "title": PROJECT_TITLE
    })

@app.post("/generate-tests")
async def generate_tests(request: Request, context: str = Form(...)):
    result = logic.generate_tests(context)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result,
        "title": PROJECT_TITLE
    })
