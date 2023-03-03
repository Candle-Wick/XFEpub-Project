class BadRequestException(Exception):

    def __init__(self, error_type: str, *args: object) -> None:
        self.error_type = error_type 
        super().__init__(*args)