from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import cv2
import asyncio
from router.i_interface import router as api_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001, debug=True)





