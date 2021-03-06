import json
from .util import sort_slots_with_key


class UserAct:
    """
    User Dialogue Acts
    """
    INFORM = "inform"
    AFFIRM = "affirm"
    NEGATE = "negate"

    @staticmethod
    def confirm_acts():
        """
        Actions that are responses to system's confirm
        """
        return [UserAct.AFFIRM, UserAct.NEGATE]

    @staticmethod
    def intent_acts():
        """
        Actions that are in the image editing domain
        """
        return [UserAct.INFORM]


class SystemAct:
    """
    System dialogue acts
    """
    GREETING = "greeting"
    INFORM = "inform"
    REQUEST = "request"
    CONFIRM = "confirm"
    QUERY = "query"
    EXECUTE = "execute"
    BYE = "bye"


class SysIntent(object):
    """
    A utility object for system intent slots
    """

    def __init__(self,
                 confirm_slots=None,
                 request_slots=None,
                 query_slots=None,
                 execute_slots=None):
        """
        default argument cannot be list -> a bug that fucked me for 2 days...
        """
        if confirm_slots is None:
            confirm_slots = []
        if request_slots is None:
            request_slots = []
        if query_slots is None:
            query_slots = []
        if execute_slots is None:
            execute_slots = []
        self.confirm_slots = confirm_slots
        self.request_slots = request_slots
        self.query_slots = query_slots
        self.execute_slots = execute_slots

    def __iadd__(self, other_intent):
        self.confirm_slots += other_intent.confirm_slots
        self.request_slots += other_intent.request_slots
        self.query_slots += other_intent.query_slots
        self.execute_slots += other_intent.execute_slots
        return self

    def __add__(self, other_intent):
        confirm_slots = self.confirm_slots + other_intent.confirm_slots
        request_slots = self.request_slots + other_intent.request_slots
        query_slots = self.query_slots + other_intent.query_slots
        execute_slots = self.execute_slots + other_intent.execute_slots
        return SysIntent(confirm_slots, request_slots, query_slots,
                         execute_slots)

    def __radd__(self, other_intent):
        return other_intent.__add__(self)

    def __eq__(self, other_intent):
        """
        Compare slots, regardless of order
        """
        if sort_slots_with_key('slot',
                               self.confirm_slots) != sort_slots_with_key(
                                   'slot', other_intent.confirm_slots):
            return False
        if sort_slots_with_key('slot',
                               self.request_slots) != sort_slots_with_key(
                                   'slot', other_intent.request_slots):
            return False
        if sort_slots_with_key('slot',
                               self.query_slots) != sort_slots_with_key(
                                   'slot', other_intent.query_slots):
            return False
        if sort_slots_with_key('slot',
                               self.execute_slots) != sort_slots_with_key(
                                   'slot', other_intent.execute_slots):
            return False
        return True

    def empty(self):
        if len(self.confirm_slots) != 0:
            return False
        elif len(self.request_slots) != 0:
            return False
        elif len(self.query_slots) != 0:
            return False
        elif len(self.execute_slots) != 0:
            return False
        return True

    def clear(self):
        self.confirm_slots.clear()
        self.request_slots.clear()
        self.query_slots.clear()
        self.execute_slots.clear()

    def copy(self):
        return SysIntent(self.confirm_slots, self.request_slots,
                         self.query_slots, self.execute_slots)

    def to_json(self):
        obj = {
            'confirm': self.confirm_slots,
            'request': self.request_slots,
            'query': self.query_slots,
            'execute': self.execute_slots
        }
        return obj

    def from_json(self, obj):
        self.confirm_slots = obj['confirm']
        self.request_slots = obj['request']
        self.query_slots = obj['query']
        self.executable_slots = obj['execute']

    def pprint(self):
        print('confirm', self.confirm_slots)
        print('request', self.request_slots)
        print('query', self.query_slots)
        print('execute', self.execute_slots)

    def executable(self):
        """
        Returns True iff all slots are executable
        """
        if len(self.confirm_slots) != 0:
            return False
        if len(self.request_slots) != 0:
            return False
        if len(self.query_slots) != 0:
            return False
        if len(self.execute_slots) != 0:
            return True
        return False
