from fastapi import FastAPI
import word_vectors
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from frontend
origins = [
    "http://localhost:3000",  # React's default development server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Default endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/giveup/{game_id}")
async def fetch_word(game_id: int):
    target_word = await word_vectors.get_target_word(game_id)
    return {"word": target_word}

@app.get("/api/guess/{game_id}/{word}")
async def fetch_word(game_id: int, word: str):
    return await word_vectors.get_word_info(game_id, word)

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