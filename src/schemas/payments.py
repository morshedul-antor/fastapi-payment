from lib2to3.pgen2.token import OP
from optparse import Option
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentBase(BaseModel):
    order_amount: Optional[str] = None
    payment_status: Optional[str] = None
    remarks: Optional[str] = None


class PaymentIn(PaymentBase):
    receiver_id: Optional[int] = None
    service_id: Optional[int] = None
    trx_id: Optional[str] = None


class PaymentOut(PaymentIn):
    id: Optional[int] = None
    service_id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class PaymentUpdate(PaymentBase):
    pass
