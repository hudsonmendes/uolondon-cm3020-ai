from typing import Union

from unittest.mock import patch, Mock
import unittest
import random

from motor import Motor
from phenotype import PhenotypeWaveForm


class MotorTest(unittest.TestCase):

    def test_class_exists(self):
        self.assertIsNotNone(Motor)

    @patch("phenotype.Phenotype")
    def test_parse_from_phenotype(self, MockPhenotype: Mock):
        waveform, amp, freq = PhenotypeWaveForm.PULSE, random.random(), random.random()
        MockPhenotype.return_value.control_waveform = waveform
        MockPhenotype.return_value.control_amp = amp
        MockPhenotype.return_value.control_freq = freq
        actual = Motor.generate_from(MockPhenotype())
        self.assertEqual(waveform, actual.waveform)
        self.assertEqual(amp, actual.amp)
        self.assertEqual(freq, actual.freq)
