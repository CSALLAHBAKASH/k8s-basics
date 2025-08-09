from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.get('/')
def home():
    return {"message": "Hello World v2"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
