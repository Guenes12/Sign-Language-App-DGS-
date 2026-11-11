from fastapi import FastAPI
from app.api.prediction import router


app = FastAPI(

    title="DGS Recognition API",

    version="1.0"

)

app.include_router(router)


@app.get("/")

def health():

    return {

        "status": "running"

    }
 