from classes.BaseRobot import BaseRobot


class BiscointRobot(BaseRobot):
    def __init__(self, biscoint_api):
        super().__init__()
        self.api = biscoint_api

    def get_offer(self, op: str, amount: float, is_quote: bool, base='BTC', quote='BRL'):
        return self.api.get_offer(op=op, amount=amount, isQuote=is_quote, base=base, quote=quote)

    def confirm_offer(self, offer_id: str):
        executed = self.api.confirm_offer(offer_id)
        super().confirm_offer(executed)
