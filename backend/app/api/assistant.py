
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.groq_service import get_ai_response

router = APIRouter()


class AssistantRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000
    )


class AssistantResponse(BaseModel):
    answer: str


@router.post("/ask", response_model=AssistantResponse)
def ask_assistant(
    request: AssistantRequest,
    db: Session = Depends(get_db)
):

    try:
        answer = get_ai_response(request.message, db)

        return {
            "answer": answer
        }

    except Exception as e:
        print(f"Assistant Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="AI assistant failed to generate a response"
        )
