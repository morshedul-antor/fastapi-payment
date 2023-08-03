import string
import random
import time


class RandomString:

    @staticmethod
    def random_trx(size, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def current_millisecond():
        return round(time.time() * 1000)
