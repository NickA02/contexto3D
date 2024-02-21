import spacy
from sklearn.decomposition import PCA
import numpy as np 
from pydantic import BaseModel
from httpx import AsyncClient

# Load the pre-trained spaCy model
nlp = spacy.load("en_core_web_md")
pca = PCA(n_components=3)
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
def project_vector_3d(vector):
    """Transform Word Vector into 3 Dimensions"""
    # Assuming 'vectors' is a list of high-dimensional vectors
    return pca.fit_transform(vector)

async def get_target_word(game_id: int) -> str:
    """Call Contexto API to retrieve today's word based on the game ID."""
    async with AsyncClient() as client:
        response = await client.get(f"https://api.contexto.me/machado/en/giveup/{game_id}")
        data = response.json()
        return data.get("word", "")  # Return an empty string if 'word' is not found

def get_req_word_contexto() -> tuple:
    """Call Contexto API to retrieve info about a guessed word"""
    #TODO
    rank: str
    word: str
    lemma: str
    err: str
    if 1: #TODO
        #On Success
        return (rank, word, lemma)
    else:
        #On Err
        return (err)

def get_relative_vector_3d(word) -> list:
    """Determine relative vector between request word and target word"""
    target_word = get_target_word()
    target_vector = get_word_vector(target_word)

    req_vector = get_word_vector(word)

    distance_vector = req_vector - target_vector
    relative_vector_3D = project_vector_3d(distance_vector)
    
    return relative_vector_3D



def get_word_info(word: str):
    """Package word information into a returnable dataframe"""
    #Assuming success
    rank, word, lemma = get_req_word_contexto()

    vector = get_relative_vector_3d()

    return Word()
    #else:
    #    raise Exception(f"Word ({word}) does not exist, or is otherwise not supported.")
