from fastapi import FastAPI, HTTPException
import os
from static_files import StaticFileMiddleware
from word_vectors import Word
import word_vectors
import requests
from httpx import AsyncClient

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/get-word")
async def fetch_word():
    async with AsyncClient() as client:
        response = await client.get("https://api.contexto.me/machado/en/giveup/520")
        return response.json()

# @app.post("/api/get_word")
# def set_word(word: str) -> Word:
#     """Set Word and calculate dictionary of lookup-able words"""
#     try:
#         return word_vectors.get_word_info(word)
#     except Exception as e:
#         return HTTPException(status_code=502)

# url = "http://localhost:8000/api/get_word"
# data = {"word": "example"}
# headers = {"Content-Type": "application/json"}

# response = requests.put(url, json=data, headers=headers)
# print(response.status_code)
# print(response.json())