class PublicKey:
    def __init__(self, p: int, g: int, y: int):
        self.p: int = p
        self.g: int = g
        self.y: int = y