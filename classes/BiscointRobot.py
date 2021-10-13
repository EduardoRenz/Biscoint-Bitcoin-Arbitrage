from classes.BaseRobot import BaseRobot
from biscoint_api_python import Biscoint
from configs import API_KEY, API_SECRET

class BiscointRobot(BaseRobot):
    def __init__(self, api=Biscoint):
        super().__init__()
        self.api = api(API_KEY, API_SECRET)

    def get_offer(self, op: str, amount: str, is_quote: bool, base='BTC', quote='BRL'):
        return self.api.get_offer(op=op, amount=amount, isQuote=is_quote, base=base, quote=quote)

    def confirm_offer(self, offer_id: str):
        executed = self.api.confirm_offer(offer_id)
        super().confirm_offer(executed)
