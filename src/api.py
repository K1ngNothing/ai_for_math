from coordinator import Coordinator
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from logTools import LogLevel


app = FastAPI(title="Math Multi-Agent ML Service")


def solve_task(statement: str) -> dict | None:
    """
    Solves task with given statement.
    Returns either:
        * dict with 'solution' and 'answer' fields, if solving was successful
        * None if agents failed to solve the problem
    """

    try:
        coordinator = Coordinator(LogLevel.RELEASE)
        result = coordinator.solve(statement)
        return {
            'solution': result['solution'],
            'answer': result['answer']
        }
    except Exception:
        return None


@app.post("/forward")
async def forward(request: Request):
    """
    Handler for POST /forward
    Expected request format:
    {
        "statement": str -- statement for the problem
    }
    Return format:
    {
        'solution': str -- solution for the problem,
        'answer': str -- answer for the problem,
    }
    """

    content_type = request.headers.get("content-type", "")
    if "application/json" not in content_type:
        raise HTTPException(status_code=400, detail="bad request")

    try:
        payload = await request.json()
        task_statement = payload['statement']
    except Exception:
        raise HTTPException(status_code=400, detail="bad request")

    result = solve_task(task_statement)
    if result is None:
        raise HTTPException(
            status_code=403,
            detail="model failed to solve the task"
        )
    return JSONResponse(content=result)
