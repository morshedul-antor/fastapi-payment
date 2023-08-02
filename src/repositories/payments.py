from models import Payment
from schemas import PaymentIn, PaymentUpdate
from repositories import BaseRepo

payments_repo = BaseRepo[Payment, PaymentIn, PaymentUpdate](Payment)
