
from fastapi import Header, HTTPException

def validate_authorization_header(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid Authorization header format.")
    return authorization

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import httpx

app = FastAPI()

class Item(BaseModel):
    title: str
    description: str

@app.post("/send-data-with-headers/")
async def send_data_with_headers(item: Item, authorization: str = Depends(validate_authorization_header)):
    url = "https://jsonplaceholder.typicode.com/posts"  # Example external API URL
    
    # Prepare headers to send to the external API
    headers = {
        'Content-Type': 'application/json',
        'Authorization': authorization  # Using validated Authorization header
    }
    
    # Send POST request to the external API
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=item.dict(), headers=headers)
        if response.status_code != 201:
            raise HTTPException(status_code=400, detail="Error sending data to external API")
        return response.json()
