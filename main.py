from convolutional_code import ConvolutionalCode
from encoder import encode
from decoder import viterbi_decode
import random

def run_demo():
    conv = ConvolutionalCode((5, 7))
    input_bytes = b"\xFE\xF0\x0A\x01"
    encoded = encode(input_bytes, conv)
    decoded, corrected = viterbi_decode(encoded, conv)
    print(f"Decoded correctly: {decoded == input_bytes}, Errors corrected: {corrected}")

    # Introduce noise
    corrupted = encoded.copy()
    for _ in range(5):
        idx = random.randint(0, len(corrupted) - 1)
        corrupted[idx] ^= 1
    decoded, corrected = viterbi_decode(corrupted, conv)
    print(f"Decoded after corruption: {decoded == input_bytes}, Errors corrected: {corrected}")

if __name__ == "__main__":
    run_demo()
