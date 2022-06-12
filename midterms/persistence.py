from dataclasses import dataclass
from typing import List, Union, Optional

from pathlib import Path

import logging
LOGGER = logging.getLogger(__name__)


@dataclass
class PersistenceSettings:
    folder: Path


class DnaRepository:
    settings: PersistenceSettings

    def __init__(self, settings: PersistenceSettings):
        self.settings = settings

    def read(self, species: str, individual: Optional[int] = None):
        if not individual:
            individual = 0
        filename = self.settings.folder / f"{species}.dna"
        with open(filename, 'r+', encoding='utf-8') as fh:
            for i, line in enumerate(fh):
                if i == individual:
                    LOGGER.info(f"DNA, {species}.dna, reading line {individual}: {line}")
                    return line
        return None

    def write(self, species: str, dna_code: Union[List[float], str], override: bool = False):
        filename = self.settings.folder / f"{species}.dna"
        with open(filename, 'w+' if override else 'a+', encoding='utf-8') as fh:
            line = dna_code if isinstance(dna_code, str) else ",".join([str(base) for base in dna_code])
            fh.write(f"{line}\n")
            LOGGER.info(f"DNA, {species}.dna, {'overriden' if override else 'appended'}: {line}")
