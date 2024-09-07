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
