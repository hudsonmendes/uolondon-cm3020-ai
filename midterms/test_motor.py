import unittest
from unittest.mock import patch
from hypothesis import given
from hypothesis.strategies import sampled_from, floats, integers

from numpy import pi

from motor import Motor
from phenotype import PhenotypeWaveForm


class MotorTest(unittest.TestCase):

    def test_class_exists(self):
        self.assertIsNotNone(Motor)

    @given(sampled_from(PhenotypeWaveForm), floats(allow_nan=False), floats(allow_nan=False))
    def test_parse_from_phenotype(self, waveform: PhenotypeWaveForm, amp: float, freq: float):
        with patch("phenotype.Phenotype") as MockPhenotype:
            MockPhenotype.return_value.control_waveform = waveform
            MockPhenotype.return_value.control_amp = amp
            MockPhenotype.return_value.control_freq = freq
            actual = Motor.generate_from(MockPhenotype())
            self.assertEqual(waveform, actual.waveform)
            self.assertEqual(amp, actual.amp)
            self.assertEqual(freq, actual.freq)

    @given(integers(1, 100))
    def test_next_pulse_amp_1_freq_pi(self, n):
        motor = Motor(waveform=PhenotypeWaveForm.PULSE, amp=1., freq=pi)
        for _ in range(n):
            self.assertEqual(-1., next(motor))
            self.assertEqual(+1., next(motor))

    @given(integers(1, 100), floats(2., 5.))
    def test_next_pulse_amp_x_freq_pi(self, n: int, amp: float):
        motor = Motor(waveform=PhenotypeWaveForm.PULSE, amp=amp, freq=pi)
        for _ in range(n):
            self.assertEqual(-amp, next(motor))
            self.assertEqual(+amp, next(motor))

    @given(integers(1, 100))
    def test_next_pulse_amp_1_freq_half_pi(self, n):
        motor = Motor(waveform=PhenotypeWaveForm.PULSE, amp=1., freq=pi/2)
        for _ in range(n):
            self.assertEqual(+1., next(motor))
            self.assertEqual(-1., next(motor))
            self.assertEqual(-1., next(motor))
            self.assertEqual(+1., next(motor))

    @given(integers(1, 100), floats(2., 5.))
    def test_next_pulse_amp_x_freq_half_pi(self, n: int, amp: float):
        motor = Motor(waveform=PhenotypeWaveForm.PULSE, amp=amp, freq=pi/2)
        for _ in range(n):
            self.assertEqual(+amp, next(motor))
            self.assertEqual(-amp, next(motor))
            self.assertEqual(-amp, next(motor))
            self.assertEqual(+amp, next(motor))