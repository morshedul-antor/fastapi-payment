from models import Payment
from schemas import PaymentIn, PaymentUpdate
from repositories import payments_repo
from services import BaseService
from exceptions import ServiceResult, AppException
from sqlalchemy.orm import Session
from db import settings
from utils import RandomString

import requests


class PaymentService(BaseService[Payment, PaymentIn, PaymentUpdate]):

    async def payment_process(self, db: Session, user_id: int, service_id: int, amount: str):
        payment_url = settings.GATEWAY_URL
        trx_id = RandomString.random_trx(10)

        payment_data = payments_repo.create(db=db, data_in=PaymentIn(
            receiver_id=user_id,
            service_id=service_id,
            trx_id=trx_id,
            order_amount=amount
        ))

        if not payment_data:
            return ServiceResult(AppException.ServerError("Something went wrong!"))
        else:
            payload = {
                "store_id": settings.STORE_ID,
                "signature_key": settings.SIGNATURE_KEY,
                "success_url": "http://localhost:3000/success",
                "fail_url": "http://www.merchantdomain.com/failedpage.html",
                "cancel_url": "http://www.merchantdomain.com/cancelpage.html",
                "amount": amount,
                "tran_id": trx_id,
                "currency": "BDT",
                "desc": "Merchant Payment",
                "cus_name": "Customer",
                "cus_email": "customer@gmail.com",
                "cus_add1": "Dhaka",
                "cus_add2": "Dhaka",
                "cus_city": "Dhaka",
                "cus_state": "Dhaka",
                "cus_postcode": "1215",
                "cus_country": "Bangladesh",
                "cus_phone": "+8801700000000",
                "type": "json"
            }

            try:
                # Make a POST request to AamarPay API
                response = requests.post(payment_url, json=payload)

                if response.status_code == 200:
                    result = response.json()
                    result.update({"trx_id": trx_id})
                    return result
                else:
                    return {"context": "Gateway Failed!", "status_code": response.status_code}
            except requests.exceptions.RequestException as e:
                return {"context": "Failed to connect AamarPay API!", "error": str(e)}

    async def payment_details(self, db: Session, trx_id: str):
        payment_details_url = f'{settings.DETAILS_URL}?request_id={trx_id}&store_id={settings.STORE_ID}&signature_key={settings.SIGNATURE_KEY}&type=json'

        try:
            # Make a POST request to AamarPay API for payment details
            response = requests.post(payment_details_url)

            if response.status_code == 200:
                result = response.json()
                service_id = payments_repo.get_by_key_first(
                    db=db, trx_id=trx_id).id

                update = payments_repo.update(db=db, id=service_id, data_update=PaymentUpdate(
                    payment_status=result["status_title"]
                ))
                return result
            else:
                return {"context": "Gateway Failed!", "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"context": "Failed to connect AamarPay API!", "error": str(e)}


payments_service = PaymentService(Payment, payments_repo)
