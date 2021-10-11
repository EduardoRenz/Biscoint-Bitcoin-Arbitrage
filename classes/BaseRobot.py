from configs import logging
import random
import string

OPS = ['buy', 'sell']


class BaseRobot():
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def _generateRandomId(self, size=17):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))

    def get_offer(self, op: OPS, amount: str, is_quote: bool, base='BTC', quote='BRL'):
        self.logger.info(f'{__name__}.get_offer()')
        return None

    def confirm_offer(self, executed):
        self.logger.info(executed)
        return None
