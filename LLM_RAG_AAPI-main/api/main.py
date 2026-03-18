from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import importlib
import time
from typing import Dict, Any

from .models import ExecuteRequest, ExecuteResponse

from embeddings.vector_store import VectorStore

from .utils import log_execution

app = FastAPI()
vector_store = VectorStore()

@app.post("/execute", response_model=ExecuteResponse)
async def execute(request: ExecuteRequest) -> Dict[str, Any]:
    start_time = time.time()
    
    # Phase 1: Function Retrieval
    function_name = vector_store.retrieve_function(request.prompt)
    if not function_name:
        error_msg = f"No function matching prompt: '{request.prompt}'"
        log_execution(
            func_name="N/A",
            success=False,
            execution_time=(time.time() - start_time) * 1000,
            error=error_msg
        )
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "error": error_msg
            }
        )

    try:
        module = importlib.import_module("automation_functions.functions")
        func = getattr(module, function_name)
        
        # Special handling for shell commands
        if function_name == "run_shell_command":
            result = func(request.prompt)
        else:
            result = func()
            
        exec_time = (time.time() - start_time) * 1000
        log_execution(function_name, True, exec_time)
        
        return {
            "status": "success",
            "function": function_name,
            "result": str(result),
            "execution_time_ms": exec_time
        }
        
    except Exception as e:
        exec_time = (time.time() - start_time) * 1000
        error_msg = f"Execution failed: {str(e)}"
        log_execution(function_name, False, exec_time, error_msg)
        
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "function": function_name,
                "error": error_msg,
                "execution_time_ms": exec_time
            }
        )