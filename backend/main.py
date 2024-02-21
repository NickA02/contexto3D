from fastapi import FastAPI, HTTPException
import os
from static_files import StaticFileMiddleware
from word_vectors import Word
import word_vectors

app = FastAPI()

@app.put("/api/get_word")
def set_word(word: str) -> Word:
    """Set Word and calculate dictionary of lookup-able words"""
    try:
        return word_vectors.get_word_info(word)
    except Exception as e:
        return HTTPException(status_code=502)

app.mount("/", StaticFileMiddleware("../static", "index.html"))