# test_convolutional_code.py

import unittest
from encoder import encode
from decoder import viterbi_decode

class TestConvolutionalCode(unittest.TestCase):

    def test_basic_case(self):
        input_bits = [1, 0, 1, 1, 0, 0, 1]
        encoded = encode(input_bits)
        decoded = viterbi_decode(encoded)
        self.assertEqual(decoded, input_bits)

    def test_empty_input(self):
        input_bits = []
        encoded = encode(input_bits)
        decoded = viterbi_decode(encoded)
        self.assertEqual(decoded, input_bits)

    def test_all_zeros(self):
        input_bits = [0] * 10
        encoded = encode(input_bits)
        decoded = viterbi_decode(encoded)
        self.assertEqual(decoded, input_bits)

    def test_all_ones(self):
        input_bits = [1] * 10
        encoded = encode(input_bits)
        decoded = viterbi_decode(encoded)
        self.assertEqual(decoded, input_bits)

if __name__ == '__main__':
    unittest.main()
