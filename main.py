from fastapi import FastAPI, HTTPException
from user import User
import storage
import os
from checkin import CheckinRequest, Checkin
from static_files import StaticFileMiddleware
from word_vectors import Word1
import word_vectors

app = FastAPI()


@app.get("/api/registrations")
def get_registrations() -> list[User]:
    return storage.get_registrations()


@app.post("/api/registrations")
def new_registration(user: User) -> User:
    try:
        return storage.create_registration(user)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post("/api/reset")
def reset() -> str:
    """Development-only route for resetting storage module and adding fake user and checkin."""
    if "MODE" in os.environ and os.environ["MODE"] == "production":
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        storage.reset()
        storage.create_registration(User(pid=710453084, first_name="Kris", last_name="Jordan"))
        storage.create_checkin(710453084)
        return "OK"

@app.post("/api/checkin")
def new_checkin(request: CheckinRequest) -> Checkin:
    """Route for making a check in request and send final check in"""
    #raise HTTPException(status_code=422, detail=str(pid))
    try:
        return storage.create_checkin(request.pid)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    
@app.get("/api/checkin")
def get_checkin() -> list[Checkin]:
    """Route for getting checkins."""
    return storage.get_checkins()

@app.delete("/api/removeuser/{pid}")
def delete_user(pid: int) -> User:
   return storage.delete_user(pid)

@app.post("/api/reset")
def reset() -> str:
    """Development-only route for resetting storage module and adding fake user and checkin."""
    if "MODE" in os.environ and os.environ["MODE"] == "production":
        raise HTTPException(status_code=404, detail="Not Found")
    else:
        storage.reset()
        storage.create_registration(User(pid=710453084, first_name="Kris", last_name="Jordan"))
        storage.create_checkin(710453084)
        return "OK"

@app.put("/api/get_word")
def set_word(word: str) -> Word1:
    """Set Word and calculate dictionary of lookup-able words"""
    try:
        return word_vectors.get_word_info(word)
    except Exception as e:
        return HTTPException(status_code=502)

app.mount("/", StaticFileMiddleware("../static", "index.html"))