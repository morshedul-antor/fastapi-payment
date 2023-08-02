from fastapi import APIRouter, Depends
from schemas import PaymentIn
from services import payments_service
from sqlalchemy.orm import Session
from exceptions import handle_result
from db import get_db


router = APIRouter()


@router.post('/')
async def payment_gateway():
    result = await payments_service.process_transaction()
    return result
