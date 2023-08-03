from fastapi import APIRouter, Depends
from schemas import PaymentIn
from services import payments_service
from sqlalchemy.orm import Session
from exceptions import handle_result
from db import get_db


router = APIRouter()


@router.post('/')
async def payment_gateway(user_id: int, service_id: int, amount: str, db: Session = Depends(get_db)):
    result = await payments_service.payment_process(db=db, user_id=user_id, service_id=service_id, amount=amount)
    return result


@router.get('/details/{trx_id}')
async def payment_details(trx_id: str, db: Session = Depends(get_db)):
    result = await payments_service.payment_details(db=db, trx_id=trx_id)
    return result
