class Order:
    """
    The Order class represents a delivery order in a  delivery system.
    Each order has a source (pickup location), a destination (delivery location),
    and two flags indicating whether the order has been picked up and delivered.
    """

    def __init__(self, source, destination):
        """
        Initializes an Order object with a source and destination.
        """
        self.source = source
        self.destination = destination
        self.pickup = False
        self.delivered = False

    def mark_as_pickup(self):
        """
         Marks the order as picked up.
        """
        self.pickup = True
    def mark_as_delivered(self):
        """
         Marks the order as delivered.
        """
        self.delivered = True
