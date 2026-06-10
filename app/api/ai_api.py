from fastapi import APIRouter, Depends, HTTPException, status
from uuid_utils import uuid4
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession 
from app.ai.agent import CRMChainService
from app.schemas.aiSchema import ChatRequest
from app.ai.exceptions import (
    ForbiddenQueryException,
    SQLExecutionException, 
    LLMException,
    RedisConnectionException
)
router=APIRouter(prefix='/ai', tags=['Ai'])


@router.post("/chat")
async def ai_chat(payload: ChatRequest, db: AsyncSession = Depends(get_db)):
    crm_service = CRMChainService(db_session=db)
    session_id = payload.session_id or str(uuid4())
    try:
        answer = await crm_service.chat(session_id=session_id, message=payload.message)
        return {"answer": answer, "session_id": session_id}

    except ForbiddenQueryException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This question cannot be answered — it may involve data modification."
        )
    except SQLExecutionException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to execute the generated SQL query. Please rephrase your question."
        )
    except LLMException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service is temporarily unavailable. Step: {e.step}"
        )
    except RedisConnectionException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chat history service is unavailable. Please try again later."
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )