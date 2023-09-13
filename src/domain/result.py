class Result:
    def __init__(self, status_code) -> None:
        print('\tResult.__init__(self, status_code)')
        self.status_code = status_code

    def __str__(self) :
        return f'Result: (status_code={self.status_code})'
