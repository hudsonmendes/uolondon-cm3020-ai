from typing import List


class Dna:
    code: List[float]

    def __init__(self, code=[]) -> None:
        self.code = code
