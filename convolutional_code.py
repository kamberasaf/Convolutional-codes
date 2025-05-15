from typing import List
from encoder import encode
from decoder import viterbi_decode

class ConvolutionalCode:
    """The code assumes zero state termination, and k=1"""

    def __init__(self, generators: tuple):
        self.gen = gnrs(generators)
        self.K = len(max(self.gen, key=len)) - 1
        self.regi = [0] * self.K

    def gen_op(self, s):
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
        return ''.join(str(i) for i in data)


def xor(*kwargs) -> int:
    return int(sum(kwargs) % 2 == 1)


def gnrs(gnr: tuple) -> list:
    k = [bin(i).replace('0b', '') for i in gnr]
    s = max(k, key=len)
    for i, b in enumerate(k[:]):
        if len(b) < len(s):
            b = '0' * (len(s) - len(b)) + b
            k.insert(i, b)
            k.pop(i + 1)
    return k
