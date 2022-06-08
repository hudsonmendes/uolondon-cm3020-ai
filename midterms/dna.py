from typing import List


class Dna:
    code: List[float]
    gene_len: int

    def __init__(self, code: List[float], gene_len: int) -> None:
        self.code = code
        self.code_len = len(code)
        self.gene_len = gene_len
        if gene_len:
            self.gene_count = self.code_len // gene_len
            if self.code_len % gene_len == 0:
                self.gene_count -= 1
        DnaCodeVoid.raise_if_applicable_from(dna_code=self.code)
        DnaGenVoid.raise_if_applicable_from(gene_len=self.gene_len)
        DnaCodeMisalignedException.raise_if_applicable_from(dna_code_len=self.code_len, gene_count=self.gene_count, gene_len=self.gene_len)

    def express(self) -> List[List[float]]:
        out: List[List[float]] = []
        for i in range(0, self.gene_count):
            gene_begin = i*self.gene_len
            gene_end = (i+1)*self.gene_len
            out.append(self.code[gene_begin:gene_end])
        return out


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


class DnaGenVoid(Exception):
    @staticmethod
    def raise_if_applicable_from(gene_len: int):
        if gene_len <= 0:
            raise DnaGenVoid(gene_len=gene_len)

    def __init__(self, gene_len: int):
        super(DnaGenVoid, self).__init__(f"""
        The `gene_len={gene_len}` cannot have length <= 0.
        """)


class DnaCodeMisalignedException(Exception):
    @staticmethod
    def raise_if_applicable_from(dna_code_len: int, gene_count: int, gene_len: int):
        if dna_code_len != (gene_count * gene_len) + gene_count:
            raise DnaCodeMisalignedException(dna_code_len=dna_code_len, gene_len=gene_len)

    def __init__(self, dna_code_len: int, gene_len: int):
        super(DnaCodeMisalignedException, self).__init__(f"""
        The DNA `code` is misaligned with the `gen_len` and is Lethal.
        `len(code)={dna_code_len}` must be formed of `(n * gene_len={gene_len}) + n` bases,
        where the `(n * gene_len)` component are the genes themselves
        and the `+ n` component is the expression control mechanism.
        """)
