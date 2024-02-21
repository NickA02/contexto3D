import spacy
from sklearn.decomposition import PCA
import numpy as np 
from pydantic import BaseModel
from httpx import AsyncClient

# Load the pre-trained spaCy model
nlp = spacy.load("en_core_web_md")
pca = PCA(n_components=2)
_word: str = "word"
projected_vectors: list
word_distances: list

class Word(BaseModel):
    word: str
    lemma: str
    rank: str
    vector: list


# Function to get a word vector
def get_word_vector(word: str):
    return nlp(word).vector

# Example: Project a list of word vectors into 3D
def project_vectors_3d(vectors):
    """Transform Word Vector into 3 Dimensions"""
    # Assuming 'vectors' is a list of high-dimensional vectors
    return pca.fit_transform(vectors)

async def get_target_word(game_id: int) -> str:
    """Call Contexto API to retrieve today's word based on the game ID."""
    async with AsyncClient() as client:
        response = await client.get(f"https://api.contexto.me/machado/en/giveup/{game_id}")
        data = response.json()
        return data.get("word", "")  # Return an empty string if 'word' is not found

async def get_req_word_contexto(game_id: int, word: str) -> tuple:
    """Call Contexto API to retrieve info about a guessed word"""
    async with AsyncClient() as client:
        response = await client.get(f"https://api.contexto.me/machado/en/game/{game_id}/{word}")
        return response.json()


async def get_relative_vector_3d(game_id: int, word: str) -> list:
    """Determine relative vector between request word and target word"""
    target_word = await get_target_word(game_id)
    target_vector = get_word_vector(target_word)

    req_vector = get_word_vector(word)

    relative_vectors_3D = project_vectors_3d([req_vector, target_vector])
    relative_vector_3D = relative_vectors_3D[0] - relative_vectors_3D[1]
    
    return relative_vector_3D



async def get_word_info(game_id: int, word: str):
    """Package word information into a returnable dataframe"""
    #Assuming success
    data = await get_req_word_contexto(game_id, word)
    if 'err' in data:
        return data
    else: 
        word = data.get("word")
        lemma = data.get("lemma")
        rank = data.get("distance")

    vector = await get_relative_vector_3d(game_id, lemma)

    return Word(word=word, lemma=lemma, rank=rank, vector=list(vector))
    #else:
    #    raise Exception(f"Word ({word}) does not exist, or is otherwise not supported.")
