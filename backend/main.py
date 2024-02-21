from fastapi import FastAPI, HTTPException
import os
from static_files import StaticFileMiddleware
from word_vectors import Word
import word_vectors
from httpx import AsyncClient

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/giveup/{game_id}")
async def fetch_word(game_id: int):
    target_word = await word_vectors.get_target_word(game_id)
    return {"word": target_word}

@app.get("/api/guess/{game_id}/{word}")
async def fetch_word(game_id: int, word: str):
    async with AsyncClient() as client:
        response = await client.get(f"https://api.contexto.me/machado/en/game/{game_id}/{word}")
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