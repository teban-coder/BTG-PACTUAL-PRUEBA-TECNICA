from fastapi import APIRouter, HTTPException
from app.db import users_collection
from app.auth import verify_password, create_access_token

router = APIRouter()

@router.post("/login")
def login(user_id: str, password: str):
    user = users_collection.find_one({"_id": user_id})

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = create_access_token({
        "sub": user_id,
        "role": user["role"]
    })

    return {"access_token": token}