from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from router.i_interface import router as api_router

app = FastAPI()
sub_app = FastAPI(debug=True,title="sup cloud api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(api_router)
sub_app.include_router(api_router)

app.mount("/api_sup", sub_app)
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
