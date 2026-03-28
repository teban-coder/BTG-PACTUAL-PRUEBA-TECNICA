from fastapi import APIRouter, HTTPException
from app.db import users_collection, funds_collection, transactions_collection
from app.auth import require_role
from app.auth import verify_token
from fastapi import Depends
from app.exceptions import AppException
from app.services.notification_service import send_notification
import uuid

router = APIRouter()

from app.auth import hash_password

@router.get("/init-funds")
def init_funds():
    funds = [
        {"id": 1, "name": "FPV_BTG_PACTUAL_RECAUDADORA", "min_amount": 75000, "category": "FPV"},
        {"id": 2, "name": "FPV_BTG_PACTUAL_ECOPETROL", "min_amount": 125000, "category": "FPV"},
        {"id": 3, "name": "DEUDAPRIVADA", "min_amount": 50000, "category": "FIC"},
        {"id": 4, "name": "FDO-ACCIONES", "min_amount": 250000, "category": "FIC"},
        {"id": 5, "name": "FPV_BTG_PACTUAL_DINAMICA", "min_amount": 100000, "category": "FPV"},
    ]

    funds_collection.insert_many(funds)
    return {"mensaje": "Fondos insertados"}

@router.get("/init-user")
def init_user():
    user = {
        "_id": "1",
        "name": "Esteban",
        "password": hash_password("1234"),
        "role": "user",
        "notification": "email",
        "balance": 500000,
        "subscriptions": []
    }

    users_collection.insert_one(user)
    return {"mensaje": "Usuario creado"}

@router.get("/init-admin")
def init_user():
    user = {
        "_id": "2",
        "name": "Juan",
        "password": hash_password("1234"),
        "role": "admin",
        "notification": "email",
        "balance": 500000,
        "subscriptions": []
    }

    users_collection.insert_one(user)
    return {"mensaje": "Usuario creado"}

@router.post("/subscribe/{user_id}/{fund_id}")
def subscribe(user_id: str, fund_id: int, payload: dict = Depends(require_role("user"))):

    user = users_collection.find_one({"_id": user_id})
    fund = funds_collection.find_one({"id": fund_id})

    if not user or not fund:
        raise AppException(404, "Usuario no encontrado")

    if user["balance"] < fund["min_amount"]:
        raise HTTPException(
            status_code=400,
            detail=f"No tiene saldo disponible para vincularse al fondo {fund['name']}"
        )

    users_collection.update_one(
        {"_id": user_id},
        {
            "$inc": {"balance": -fund["min_amount"]},
            "$push": {
                "subscriptions": {
                    "fund_id": fund_id,
                    "amount": fund["min_amount"]
                }
            }
        }
    )

    transactions_collection.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "type": "subscription",
        "fund_id": fund_id,
        "amount": fund["min_amount"]
    })

    send_notification(user, f"Te suscribiste al fondo {fund['name']}")

    return {"mensaje": "Suscripción exitosa"}


@router.post("/unsubscribe/{user_id}/{fund_id}")
def unsubscribe(user_id: str, fund_id: int, current_user: str = Depends(verify_token)):
    user = users_collection.find_one({"_id": user_id})

    if not user:
        raise AppException(404, "Usuario no encontrado")

    sub = next((s for s in user["subscriptions"] if s["fund_id"] == fund_id), None)

    if not sub:
        raise AppException(404, "No estas suscrito a este fondo")

    users_collection.update_one(
        {"_id": user_id},
        {
            "$inc": {"balance": sub["amount"]},
            "$pull": {"subscriptions": {"fund_id": fund_id}}
        }
    )

    transactions_collection.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "type": "cancel",
        "fund_id": fund_id,
        "amount": sub["amount"]
    })

    return {"mensaje": "Cancelado"}

@router.get("/transactions/{user_id}")
def get_transactions(user_id: str, current_user: str = Depends(verify_token)):
    return list(transactions_collection.find({"user_id": user_id}, {"_id": 0}))

@router.get("/admin/transactions")
def get_all_transactions(payload: dict = Depends(require_role("admin"))):
    return list(transactions_collection.find({}, {"_id": 0}))