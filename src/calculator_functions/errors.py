class ParsingError(Exception):

    def __init__(self, message: str, position: None | int, error_type: str = 'Parsing'):
        super().__init__(message)
        self.message = message
        self.position = position
        self.error_type = error_type

    def __str__(self):
        if self.position is not None:
            return f"{self.error_type} error: {self.message} at position {self.position}"
        return f"{self.error_type} error: {self.message}"
