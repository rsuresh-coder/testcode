from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

class Item(BaseModel):
    title: str
    description: str

@app.post("/send-data/")
async def send_data(item: Item):
    url = "https://jsonplaceholder.typicode.com/posts"  # Example external API URL
    data = item.dict()
    headers = {'Content-Type': 'application/json'}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
        if response.status_code != 201:
            raise HTTPException(status_code=400, detail="Error sending data to external API")
        return response.json()

