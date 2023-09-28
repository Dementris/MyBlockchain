from uuid import uuid4

class Node(object):
    def __init__(self):
        self.identifier = str(uuid4()).replace('-','')
        self._coins_amount = 0

    def __repr__(self):
        return "Test a:% s b:% s" % (self._coins_amount, self._coins_amount)

    def get_coin(self,amount):
        self._coins_amount += amount
