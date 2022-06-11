from dataclasses import dataclass

from phenotype import Phenotype, PhenotypeWaveForm


@dataclass
class Motor:
    waveform: PhenotypeWaveForm
    amp: float
    freq: float

    @staticmethod
    def generate_from(phenotype: Phenotype) -> "Motor":
        return Motor(
            waveform=phenotype.control_waveform,
            amp=phenotype.control_amp,
            freq=phenotype.control_freq
        )

    
