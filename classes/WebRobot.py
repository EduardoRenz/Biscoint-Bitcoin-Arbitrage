import json
from classes.BiscointRobot import BiscointRobot


class WebRobot(BiscointRobot):
    def __init__(self, web_driver,api=None):
        if api != None:
            super().__init__(api)
        else:
            super().__init__()
            
        self.driver = web_driver

    def __genOfferParams(self, base: str, quote: str, op: str, amount: str, is_quote: bool):
        params = {"base": base, "quote": quote, "op": op, "amount": amount, "isQuote":
                 is_quote, "requestId": self._generateRandomId()}
        return params

    def get_offer(self, op: str, amount: str, is_quote: bool, base='BTC', quote='BRL'):
        try:
            offer_params = self.__genOfferParams(
                base=base, op=op, amount=amount, quote=quote, is_quote=is_quote)
            response = self.driver.execute_script(
                f"return Meteor.callAsync('ops.getOffer',{json.dumps(offer_params)})")
            return response
        except Exception as e:
            self.logger.error(f"Erro ao rodar get_offer {e}")

    def confirm_offer(self, offer_id):
        offer_param = {'offerId': offer_id}
        executed = self.driver.execute_script(f"Meteor.call('ops.confirmOffer','{json.dumps(offer_param)}')")
        self.logger.info(executed)
