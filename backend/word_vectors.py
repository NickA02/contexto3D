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
async def project_vector_3d(req_vector: str, game_id: int):
    """Transform Word Vector into 3 Dimensions"""
    async with AsyncClient() as client:
        response = await client.get(f"https://api.contexto.me/machado/en/top/{game_id}")
        data = response.json()
    vectors = []
    for word in data.get("words"):
        word_vector = get_word_vector(word)
        vectors.append(word_vector)
    pca = PCA(n_components=3)  # Assuming 'vectors' is a list of high-dimensional vectors
    pca.fit(vectors)
    change_of_basis_matrix = pca.components_.T
    word_3d = np.dot(req_vector, change_of_basis_matrix)
    #subtract from the first vector of the original list
    return 10 * (word_3d - np.dot(vectors[0], change_of_basis_matrix))

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
    req_vector = get_word_vector(word)
    vector_3d = await project_vector_3d(req_vector, game_id)
    return vector_3d



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
