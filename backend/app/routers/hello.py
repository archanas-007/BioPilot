from fastapi import APIRouter
from typing import Optional

router = APIRouter()

@router.get("/hello")
def read_hello(name: Optional[str] = None):
    if name:
        return {"message": f"Hello {name}"}
    return {"message": "Hello World"}
