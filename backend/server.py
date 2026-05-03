from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks


# ----------------------------------------------------------------------
# Preview de l'animation generee (servit en static depuis /app/repo_savard)
# ----------------------------------------------------------------------
ANIM_DIR = "/app/repo_savard/animation_output"
ANIM_HTML = os.path.join(ANIM_DIR, "animation.html")
ANIM_AUDIO_DIR = os.path.join(ANIM_DIR, "audio")


@api_router.get("/anim")
async def serve_animation_redirect():
    # Redirection vers /api/anim/ (avec slash final) pour que les URLs
    # relatives `audio/X.mp3` dans le HTML resolvent vers /api/anim/audio/X.mp3
    return RedirectResponse(url="/api/anim/", status_code=307)


@api_router.get("/anim/", response_class=HTMLResponse)
async def serve_animation():
    if not os.path.exists(ANIM_HTML):
        return HTMLResponse(
            "<h1>Animation non generee</h1>"
            "<p>Lancez : <code>python3 scripts/generate_animation.py</code></p>",
            status_code=404,
        )
    return FileResponse(
        ANIM_HTML,
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store"},
    )


@api_router.get("/anim/audio/{filename}")
async def serve_animation_audio(filename: str):
    """Sert les MP3 de narration referencees par l'animation HTML."""
    # Securite : empeche path traversal (../)
    if "/" in filename or "\\" in filename or ".." in filename:
        return HTMLResponse("Invalid filename", status_code=400)
    path = os.path.join(ANIM_AUDIO_DIR, filename)
    if not os.path.exists(path) or not filename.endswith(".mp3"):
        return HTMLResponse("Audio not found", status_code=404)
    return FileResponse(
        path,
        media_type="audio/mpeg",
        headers={"Cache-Control": "public, max-age=3600"},
    )

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()