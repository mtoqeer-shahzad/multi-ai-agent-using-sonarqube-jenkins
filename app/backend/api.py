from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.core.ai_agent import get_ai_agent_response
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

app = FastAPI(title="MULTI AI AGENT")

# --- Pydantic Schema ---
class RequestState(BaseModel):
    model_name   : str
    system_prompt: str
    messages     : List[str]  # Frontend se ["Hi", "Hello"] aa raha hai
    allow_message: bool 

# --- Endpoint ---
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from app.core.ai_agent import get_ai_agent_response
from app.config.settings import settings
from app.common.logger import get_logger



logger = get_logger(__name__)

app = FastAPI(title="Multi Agents")

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#
class RequestState(BaseModel):
    model_name   : str
    system_prompt: str
    messages     : List[str]
    allow_message: bool


@app.post("/chat")
def chat(
    request      : RequestState,
):
    try:
        if request.model_name not in settings.ALLOWED_MODEL_NAMES:
            raise HTTPException(
                status_code=400,
                detail=f"Model not allowed. Choose: {settings.ALLOWED_MODEL_NAMES}"
            )

        query = request.messages[-1]

        # ✅ User ki apni API keys use ho rahi hain — server ki nahi
        response = get_ai_agent_response(
            model_id       = request.model_name,
            query          = query,
            allow_search   = request.allow_message,
            system_prompt  = request.system_prompt,
             # user ki key
        )

        logger.info(f"Chat response sent to: {request.model_name}")
        return {"response": response}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")