from typing import Optional


class Dimensions:

    def __init__(self, width: Optional[int] = None, height: Optional[int] = None):
        if not width and not height:
            raise ValueError('One of witdh/height has to be specified')

        self.width = width
        self.height = height
