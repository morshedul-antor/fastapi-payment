from models import Payment
from schemas import PaymentIn, PaymentUpdate, PaymentDBIn
from repositories import payments_repo
from services import BaseService
from fastapi import status
from exceptions import ServiceResult, AppException
from sqlalchemy.orm import Session
from db import settings


import requests


class PaymentService(BaseService[Payment, PaymentIn, PaymentUpdate]):

    async def process_transaction(self):
        payment_url = settings.GATEWAY_URL

        payload = {
            "store_id": settings.STORE_ID,
            "signature_key": settings.SIGNATURE_KEY,
            "success_url": "http://www.merchantdomain.com/successpage.html",
            "fail_url": "http://www.merchantdomain.com/failedpage.html",
            "cancel_url": "http://www.merchantdomain.com/cancelpage.html",
            "amount": "100.0",
            "tran_id": "12312317334",
            "currency": "BDT",
            "desc": "Merchant Payment",
            "cus_name": "Name",
            "cus_email": "payer@merchantcusomter.com",
            "cus_add1": "House B-158 Road 22",
            "cus_add2": "Mohakhali DOHS",
            "cus_city": "Dhaka",
            "cus_state": "Dhaka",
            "cus_postcode": "1206",
            "cus_country": "Bangladesh",
            "cus_phone": "+8801704",
            "type": "json"
        }

        try:
            # Make a POST request to AamarPay API
            response = requests.post(payment_url, json=payload)

            if response.status_code == 200:
                result = response.json()
                return result
            else:
                return {"context": "Gateway Failed!", "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"context": "Failed to connect AamarPay API!", "error": str(e)}


payments_service = PaymentService(Payment, payments_repo)
