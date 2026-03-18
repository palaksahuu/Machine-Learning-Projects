from pydantic import BaseModel
from typing import Optional

class ExecuteRequest(BaseModel):
    prompt: str

class ExecuteResponse(BaseModel):
    status: str  # "success" or "error"
    function: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None
    execution_time_ms: Optional[float] = None