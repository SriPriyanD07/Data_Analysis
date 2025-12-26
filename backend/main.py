"""
Agentic Notebook Generator - Phase 1 MVP
FastAPI backend for EDA notebook generation
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
import shutil
from datetime import datetime

from intent_parser import IntentParser
from notebook_builder import NotebookBuilder
from code_generator import CodeGenerator

app = FastAPI(title="Agentic Notebook Generator", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Initialize components
intent_parser = IntentParser()
code_generator = CodeGenerator()
notebook_builder = NotebookBuilder()


@app.get("/")
async def root():
    return {"message": "Agentic Notebook Generator API", "version": "1.0.0", "phase": "MVP"}


@app.post("/api/generate")
async def generate_notebook(
    file: UploadFile = File(...),
    task_description: str = Form(...),
):
    """
    Generate an EDA notebook from uploaded CSV and task description
    """
    try:
        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = UPLOAD_DIR / f"{timestamp}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse intent
        print(f"📋 Parsing intent: {task_description}")
        intent = intent_parser.parse(str(file_path), task_description)
        
        # Generate notebook
        print(f"🔨 Generating notebook...")
        notebook = notebook_builder.build_eda_notebook(
            dataset_path=str(file_path),
            intent=intent,
            code_generator=code_generator
        )
        
        # Save notebook
        output_filename = f"eda_notebook_{timestamp}.ipynb"
        output_path = OUTPUT_DIR / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            import nbformat
            nbformat.write(notebook, f)
        
        print(f"✅ Notebook generated: {output_path}")
        
        return JSONResponse({
            "status": "success",
            "message": "Notebook generated successfully",
            "notebook_filename": output_filename,
            "download_url": f"/api/download/{output_filename}",
            "sections_generated": len(notebook.cells),
            "intent": intent
        })
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{filename}")
async def download_notebook(filename: str):
    """
    Download generated notebook
    """
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Notebook not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/x-ipynb+json"
    )


@app.get("/api/notebooks")
async def list_notebooks():
    """
    List all generated notebooks
    """
    notebooks = []
    for file_path in OUTPUT_DIR.glob("*.ipynb"):
        stat = file_path.stat()
        notebooks.append({
            "filename": file_path.name,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "size": stat.st_size,
            "download_url": f"/api/download/{file_path.name}"
        })
    
    return {"notebooks": sorted(notebooks, key=lambda x: x['created'], reverse=True)}


# Serve index.html at root
@app.get("/app")
async def serve_app():
    static_dir = Path(__file__).parent.parent / "frontend"
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file, media_type="text/html")
    raise HTTPException(status_code=404, detail="Frontend not found")

# Mount static files for CSS, JS
static_dir = Path(__file__).parent.parent / "frontend"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
