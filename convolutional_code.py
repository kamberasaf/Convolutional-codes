from typing import List
import itertools
import copy
from encoder import encode
from decoder import viterbi_decode

class ConvolutionalCode:
    """The code assumes zero state termination, and k=1"""

    def __init__(self, generators: tuple):
        """
        :param generators: each element in the tuple represents a single generator polynomial. The convention
        we use is: 1+D=b011=3 (and not 1+D=6)
        """
        self.gen = gnrs(generators)
        self.K = len(max(self.gen, key=len)) - 1
        self.regi = [0] * self.K

    def gen_op(self, s):
        """ This function operates the generators on a given bits. """
        shift = self.regi
        end = []
        for i in range(len(s)):
            shift.insert(0, s[i])
            for fun in self.gen:
                xor_bits = [shift[i] for i, s in enumerate(fun[::-1]) if s == '1']
                end.append(xor(*xor_bits))
            shift.pop()
        return end

    def one_bit_change(self, shift_list, num_in):
        shift = shift_list.copy()
        data = []
        shift.insert(0, num_in)
        for fun in self.gen:
            xor_bits = [shift[i] for i, s in enumerate(fun[::-1]) if s == '1']
            data.append(xor(*xor_bits))
        number = ''.join(str(i) for i in data)
        return number


def xor(*kwargs) -> int:
    sum = 0
    for num in kwargs:
        sum += num
    return int(1 == sum % 2)


def hamming_distance(s1: str, s2: str) -> str:
    return sum(s1[i] != s2[i] for i in range(len(s1)))


def gnrs(gnr: tuple) -> list:
    k = [bin(i).replace('0b', '') for i in gnr]
    s = max(k, key=len)
    for i, b in enumerate(k[:]):
        if len(b) < len(s):
            b = '0' * (len(s) - len(b)) + b
            k.insert(i, b)
            k.pop(i + 1)
    return k


if __name__ == "__main__":

    # example of constructing an encoder with constraint length = 2
    # and generators:
    #       g1(x) = 1 + x^2, represented in binary as b101 = 5
    #       g2(x) = 1 + x+ x^2, represented in binary as b111 = 7
    conv = ConvolutionalCode((5, 7))

    # encoding a byte stream
    input_bytes = b"\xFE\xF0\x0A\x01"
    encoded = conv.encode(input_bytes)
    print(encoded == [1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1,
                      1, 1])

    # decoding a byte stream
    decoded, corrected_errors = conv.decode(encoded)
    print(decoded == input_bytes)
    print(corrected_errors)

    # introduced five random bit flips
    import random

    corrupted = encoded.copy()
    for _ in range(5):
        idx = random.randint(0, len(encoded) - 1)
        corrupted[idx] = int(not (corrupted[idx]))
    decoded, corrected_errors = conv.decode(corrupted)

    print(decoded == input_bytes)
    print(corrected_errors)

    # example of constructing an encoder with constraint length = 3, and rate 1/3
    # and generators:
    #       g1(x) = 1 + x, represented in binary as b011 = 3
    #       g2(x) = 1 + x + x^2, represented in binary as b111 = 7
    #       g3(x) = 1 + x^2 + x^3, represented in binary as b1101 = 13
    conv = ConvolutionalCode((3, 7, 13))

    # encoding a byte stream
    input_bytes = b"\x72\x01"
    encoded = conv.encode(input_bytes)
    encoded = [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1]

    # decoding a byte stream
    decoded, corrected_errors = conv.decode(encoded)
    print(decoded == input_bytes)
    print(corrected_errors)

    # introduced five random bit flips
    import random

    corrupted = encoded.copy()
    for _ in range(5):
        idx = random.randint(0, len(encoded) - 1)
        corrupted[idx] = int(not (corrupted[idx]))
    decoded, corrected_errors = conv.decode(corrupted)

    print(decoded == input_bytes)
    print(corrected_errors)

    conv = ConvolutionalCode((5, 7, 27, 111, 230, 34, 52, 66, 89, 103, 153, 255))

    # encoding a byte stream
    input_bytes = b"\xFE\xF0\x0A\x01"
    encoded = conv.encode(input_bytes)
    print(encoded == [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1,
                      1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0,
                      1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1,
                      1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1,
                      0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0,
                      0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
                      1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1,
                      0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1,
                      1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1,
                      1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1,
                      1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1,
                      0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0,
                      0, 0, 0, 0, 1, 1]
          )

    # decoding a byte stream
    decoded, corrected_errors = conv.decode(encoded)
    print(decoded == input_bytes)
    print(corrected_errors)

    # introduced five random bit flips
    import random

    corrupted = encoded.copy()
    for _ in range(30):
        idx = random.randint(0, len(encoded) - 1)
        corrupted[idx] = int(not (corrupted[idx]))
    decoded, corrected_errors = conv.decode(corrupted)

    print(decoded == input_bytes)
    print(corrected_errors)
