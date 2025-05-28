from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from powerbi_service import get_embed_token, REPORT_ID

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/embed-info")
def get_embed_info():
    try:
        return get_embed_token()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
