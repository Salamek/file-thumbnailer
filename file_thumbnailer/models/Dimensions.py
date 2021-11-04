from typing import Optional


class Dimensions:

    def __init__(self, width: Optional[int] = None, height: int = 100):
        self.width = width if width else height
        self.height = height
