from .base import BMLCommand

class Event(BMLCommand):
    @BMLCommand.init_fields
    def __init__(self, start=None, message=None):
        pass
