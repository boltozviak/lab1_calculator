from typing import Any

class Token:
    def __init__(self, value: Any, position: int):
        self.value = value
        self.position = position
