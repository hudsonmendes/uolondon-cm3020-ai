from dataclasses import dataclass, is_dataclass, asdict
from abc import ABC
from typing import List, Union, Optional

import json
import os
from pathlib import Path

from dna import Dna
from evolution import Evolution, EvolutionRecord

import logging

LOGGER = logging.getLogger(__name__)


@dataclass(eq=True, frozen=True, order=True)
class PersistenceSettings:
    folder: Path


class BaseRepository(ABC):
    settings: PersistenceSettings

    def __init__(self, settings: PersistenceSettings):
        self.settings = settings

    @staticmethod
    def ensure_file_dir(filepath: Path):
        dir = filepath.parent
        if not os.path.isdir(dir):
            os.makedirs(dir)


class DnaRepository(BaseRepository):

    def __init__(self, settings: PersistenceSettings):
        super(DnaRepository, self).__init__(settings)

    def filepath(self, species: str) -> Path:
        return self.settings.folder / f"{species}.dna"

    """
    Reads and Writes DNA into files, with options to append/override
    as well as reading specific individuals from the store.
    """

    def read(self, species: str, individual: Optional[int] = None) -> Optional[Dna]:
        """
        Read a particular individual or the top one of a species DNA file.
        """
        filepath = self.filepath(species)
        self.ensure_file_dir(filepath)
        if individual is None:
            count = 0
            with open(filepath, 'r+', encoding='utf-8') as fh:
                for i, line in enumerate(fh):
                    if line:
                        count = i
            individual = count
        if os.path.isfile(filepath):
            with open(filepath, 'r+', encoding='utf-8') as fh:
                for i, line in enumerate(fh):
                    if i == individual:
                        LOGGER.info(f"DNA, {species}.dna, reading line {individual}: {line}")
                        return Dna.parse_dna(line)
        return None

    def write(self, species: str, dna_code: Union[List[float], str], override: bool = False):
        """
        Overrides or appends to a species DNA file.
        """
        filepath = self.filepath(species)
        with open(filepath, 'w+' if override else 'a+', encoding='utf-8') as fh:
            line = dna_code if isinstance(dna_code, str) else ",".join([str(base) for base in dna_code])
            fh.write(f"{line}\n")
            LOGGER.info(f"DNA, {species}.dna, {'overriden' if override else 'appended'}: {line}")

    def dedup(self, species: str):
        """
        Removes duplicated DNA from the file
        """
        filepath = self.filepath(species)
        dna_all = []
        dna_used = set()
        with open(filepath, 'r+', encoding='utf-8') as fh:
            for line in fh:
                dna_all.append(line.strip())
        with open(filepath, 'w+', encoding='utf-8') as fh:
            for dna_code in dna_all:
                if dna_code not in dna_used:
                    dna_used.add(dna_code)
                    fh.write(f"{dna_code}\n")


class EvolutionRepository(BaseRepository):
    """
    Keeps Record of the Fitness Map and Hyperparams across generations,
    so the results can be observed later.
    """

    def __init__(self, settings: PersistenceSettings):
        super(EvolutionRepository, self).__init__(settings)

    class EvolutionDecoder(json.JSONDecoder):
        def decode(self, o):
            if isinstance(o, str):
                j = json.loads(o)
                if 'elite_previous' in j and j['elite_previous']:
                    j['elite_previous'] = EvolutionRecord(**j['elite_previous'])
                j['elite_offspring'] = EvolutionRecord(**j['elite_offspring'])
                j['offspring_fitness'] = [EvolutionRecord(**ji) for ji in j['offspring_fitness']]
                return Evolution(**j)
            return super().default(o)

    class EvolutionEncoder(json.JSONEncoder):
        def default(self, o):
            if is_dataclass(o):
                return asdict(o)
            return super().default(o)

    def filepath(self, generation_id) -> Path:
        return self.settings.folder / f'generation-{generation_id}.evo'

    def read(self, generation_id: int) -> Optional[Evolution]:
        if generation_id is not None:
            filepath = self.filepath(generation_id)
            self.ensure_file_dir(filepath)
            if os.path.isfile(filepath):
                with open(filepath, 'r', encoding='utf-8') as fh:
                    return json.load(fh, cls=EvolutionRepository.EvolutionDecoder)
        return None

    def write(self, record: Evolution):
        filepath = self.filepath(record.generation_id)
        self.ensure_file_dir(filepath)
        with open(filepath, 'w+', encoding='utf-8') as fh:
            json.dump(record, fh, indent=4, cls=EvolutionRepository.EvolutionEncoder)
