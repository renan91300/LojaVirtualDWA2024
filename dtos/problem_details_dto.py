class ProblemDetailsDTO():
    def __init__(self, input: str, msg: str, type: str, loc: list[str] = None):
        self.input = input
        self.msg = msg
        self.type = type
        self.loc = loc        

    def to_dict(self):
        return self.__dict__
    