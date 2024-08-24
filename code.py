#pip install fastapi[all] langchain

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import io
from typing import Optional

# Importing Langchain loaders
from langchain.loaders import PyPDFLoader, DocxLoader

app = FastAPI()

class File(BaseModel):
    filename: str
    content: str  # base64 encoded content

@app.post("/process-file/")
async def process_file(file: File):
    # Decode the base64 content
    try:
        file_bytes = base64.b64decode(file.content)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid base64 content")

    # Check file extension and process accordingly
    if file.filename.endswith('.pdf'):
        await process_pdf(file_bytes)
    elif file.filename.endswith('.docx'):
        await process_docx(file_bytes)
    elif file.filename.endswith('.txt'):
        process_text(file_bytes)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

async def process_pdf(file_bytes: bytes):
    pdf_loader = PyPDFLoader()
    pdf_loader.load_from_file_obj(io.BytesIO(file_bytes))
    for page in pdf_loader.text_pages():
        print("PDF Page Content:", page)

async def process_docx(file_bytes: bytes):
    docx_loader = DocxLoader()
    docx_loader.load_from_file_obj(io.BytesIO(file_bytes))
    for page in docx_loader.text_pages():
        print("DOCX Page Content:", page)

def process_text(file_bytes: bytes):
    text = file_bytes.decode('utf-8')
    print("Text File Content:", text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




#####CLIENT CODE

#pip install requests


import base64
import requests

def encode_file_to_base64(file_path):
    """Encode file content to base64."""
    with open(file_path, "rb") as file:
        encoded_content = base64.b64encode(file.read()).decode('utf-8')
    return encoded_content

def send_file_to_server(file_path, url="http://localhost:8000/process-file/"):
    """Send the base64 encoded file to the server."""
    encoded_content = encode_file_to_base64(file_path)
    filename = file_path.split('/')[-1]  # Extract filename from the path
    payload = {
        "filename": filename,
        "content": encoded_content
    }
    response = requests.post(url, json=payload)
    return response

def main():
    file_path = input("Enter the path of the file to send: ")
    response = send_file_to_server(file_path)
    if response.status_code == 200:
        print("File processed successfully!")
        print("Response:", response.text)
    else:
        print("Failed to process file")
        print("Status Code:", response.status_code)
        print("Error:", response.text)

if __name__ == "__main__":
    main()
