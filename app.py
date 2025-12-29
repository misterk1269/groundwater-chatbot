from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import chatbot_api

app = FastAPI()

class Query(BaseModel):
    query: str

@app.post("/chat")
def chat_endpoint(data: Query):
    return {
        "answer": chatbot_api(data.query)
    }
