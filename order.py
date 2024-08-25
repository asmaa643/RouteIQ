class Order:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.pickup = False
        self.delivered = False

    def mark_as_pickup(self):
        self.pickup = True
    def mark_as_delivered(self):
        self.delivered = True
