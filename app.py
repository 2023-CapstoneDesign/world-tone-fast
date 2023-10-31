from fastapi import FastAPI

app = FastAPI()


@app.get("/endpoint")
def endpoint():
    return {"s3SavedKey": "dummy key"}
