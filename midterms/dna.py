from argparse import ArgumentError
from typing import List


class Dna:
    code: List[float]
    gene_len: int

    def __init__(self, code: List[float], gene_len: int) -> None:
        DnaCodeVoid.raise_if_applicable_from(dna_code=code)
        DnaCodeMisalignedException.raise_if_applicable_from(dna_code_len=len(code), gene_len=gene_len)
        self.code = code
        self.gene_len = gene_len


class DnaCodeVoid(Exception):
    @staticmethod
    def raise_if_applicable_from(dna_code: List[float]):
        if not dna_code:
            raise DnaCodeVoid(dna_code_len=len(dna_code))

    def __init__(self, dna_code_len: int):
        super(DnaCodeVoid, self).__init__(f"""
        The DNA `code` must not be void.
        `len(code)={dna_code_len}` is not a valid length.
        """)


class DnaCodeMisalignedException(Exception):
    @staticmethod
    def raise_if_applicable_from(dna_code_len: int, gene_len: int):
        if gene_len:
            gene_count = dna_code_len // gene_len
            if dna_code_len != (gene_count * gene_len) + gene_count:
                raise DnaCodeMisalignedException(dna_code_len=dna_code_len, gene_len=gene_len)

    def __init__(self, dna_code_len: int, gene_len: int):
        super(DnaCodeMisalignedException, self).__init__(f"""
        The DNA `code` is misaligned with the `gen_len` and is Lethal.
        `len(code)={dna_code_len}` must be formed of `(n * gene_len={gene_len}) + n` bases,
        where the `(n * gene_len)` component are the genes themselves
        and the `+ n` component is the expression control mechanism.
        """)
