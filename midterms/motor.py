from typing import Iterator

from numpy import pi, sin as sine

from phenotype import Phenotype, PhenotypeWaveForm


class Motor(Iterator):
    waveform: PhenotypeWaveForm
    amp: float
    freq: float
    phase: float = 0.

    def __init__(self, waveform: PhenotypeWaveForm, amp: float, freq: float):
        self.waveform = waveform
        self.amp = amp
        self.freq = freq

    @staticmethod
    def generate_from(phenotype: Phenotype) -> "Motor":
        return Motor(
            waveform=phenotype.control_waveform,
            amp=phenotype.control_amp,
            freq=phenotype.control_freq
        )

    def __iter__(self) -> "Motor":
        return self

    def __next__(self) -> float:
        output = 0.
        self.phase = (self.phase + self.freq) % (2 * pi)
        if self.waveform == PhenotypeWaveForm.PULSE:
            output = 1. if self.phase < pi else -1.
        elif self.waveform == PhenotypeWaveForm.SINE:
            output = sine(self.phase)
        return output * self.amp
