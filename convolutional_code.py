from typing import List
import itertools
import copy
from encoder import encode

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

    def decode(self, data: List[int]) -> (bytes, int):
        """
        decode data bytes. The function assumes initial and final state of encoder was at the zero state.

        :param data: coded data to be decoded, list of ints representing each received bit.
        :return: return a tuple of decoded data, and the amount of corrected errors.
        :rtype: (bytes, int)
        """
        register = self.regi.copy()
        f_bits = ''.join(str(e) for e in data)
        F_bits = [f_bits[i:i + len(self.gen)] for i in range(0, len(f_bits), len(self.gen))]
        Vit_dict_keys = [''.join(map(str, i)) for i in itertools.product([0, 1], repeat=self.K)]
        Vit_dict = {i: [] for i in Vit_dict_keys}  # counter for the The Viterbi Decoder.
        turn = 0
        while turn < len(F_bits):
            if turn == 0:
                prev = "".join(str(i) for i in register)
                op_1 = self.one_bit_change(register, 0)
                op_1_d = hamming_distance(F_bits[turn], op_1)
                Vit_dict[f'0{prev[1:]}'] = [f"{prev} -> 0{prev[:self.K - 1]}"] + [op_1_d]
                op_2 = self.one_bit_change(register, 1)
                op_2_d = hamming_distance(F_bits[turn], op_2)
                Vit_dict[f'1{prev[1:]}'] = [f"{prev} -> 1{prev[:self.K - 1]}"] + [op_2_d]
            else:
                temp_trails = []
                for path in Vit_dict.values():
                    if path:
                        register = [int(i) for i in path[-2][-self.K:]]
                        prev = "".join(str(i) for i in register)
                        op_1 = self.one_bit_change(register, 0)
                        op_1_d = hamming_distance(F_bits[turn], op_1)
                        new_path1 = path + [f"{prev} -> 0{prev[:self.K - 1]}", path[-1] + op_1_d]
                        temp_trails.append(new_path1)
                        op_2 = self.one_bit_change(register, 1)
                        op_2_d = hamming_distance(F_bits[turn], op_2)
                        new_path2 = path + [f"{prev} -> 1{prev[:self.K - 1]}", path[-1] + op_2_d]
                        temp_trails.append(new_path2)
                find_path = sorted(temp_trails, key=lambda x: x[-2][-self.K:])
                for i, best_path in enumerate(find_path):
                    try:
                        if best_path[-2][-self.K:] == find_path[i + 1][-2][-self.K:]:
                            want = min(best_path[-1], find_path[i + 1][-1])
                            if want == best_path[-1]:
                                find_path.remove(find_path[i + 1])
                                pass
                            else:
                                best_path = find_path[i + 1]
                                find_path.remove(best_path)
                                Vit_dict[best_path[-2][-self.K:]] = best_path
                                continue
                    except IndexError:
                        pass
                    Vit_dict[best_path[-2][-self.K:]] = best_path
            turn += 1
        win_order = []
        try:
            win_order = sorted(Vit_dict.items(), key=lambda x: x[-1][-1])
        except IndexError:
            for i in Vit_dict.items():
                if i:
                    win_order.append(i)
            win_order = sorted(win_order, key=lambda x: x[-1][-1])
        winner = next(iter(win_order))
        trans = [i[:self.K] for i in winner[1] if type(i) == str]
        final = []
        for index, item in enumerate(trans):
            try:
                a = f'1{item[:-1]}'
                if f'1{item[:-1]}' == trans[index + 1]:
                    final.append(1)
                else:
                    final.append(0)
            except IndexError:
                pass
        del final[-self.K + 1:]
        full = ''.join(str(e) for e in final)
        bits_8 = []
        for index in range(0, len(full), 8):
            bits_8.append(full[index: index + 8])
        decoded_bytes = bytes([int(chunk, 2) for chunk in bits_8])
        return decoded_bytes, winner[1][-1]

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
