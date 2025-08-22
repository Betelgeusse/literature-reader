from fastapi import FastAPI, APIRouter
from app.search import search_handler

app = FastAPI()
router = APIRouter()

@router.post("/search")
def method():
    try:
        return {"result": search_handler()}
    except Exception as e:
        print(f"An error has occurred: {e}")
        raise

app.include_router(router)