import uvicorn
from fastapi import FastAPI
from app.modules import modules_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(modules_router)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    return {"message": "Simple Question API Services"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)
