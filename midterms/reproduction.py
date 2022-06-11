from typing import List


class Reproduction:
    dna_code_a: List[float]
    dna_code_b: List[float]

    def __init__(
            self,
            dna_code_a: List[float],
            dna_code_b: List[float]) -> None:
        self.dna_code_a = dna_code_a
        self.dna_code_b = dna_code_b

    def reproduce(self) -> List[float]:
        return self.dna_code_a + self.dna_code_b
