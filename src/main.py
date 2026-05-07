# router.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

from src.api.api import router as api_router

app = FastAPI()

app.include_router(api_router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)