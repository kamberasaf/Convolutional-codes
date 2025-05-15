# main.py

from encoder import encode
from decoder import viterbi_decode

def main():
    # Example input bitstream
    input_bits = [1, 0, 1, 1, 0, 0, 1]

    print("Input bits:         ", input_bits)

    # Encode
    encoded_bits = encode(input_bits)
    print("Encoded bits:       ", encoded_bits)

    # Decode
    decoded_bits = viterbi_decode(encoded_bits)
    print("Decoded bits:       ", decoded_bits)

    # Check correctness
    print("Decoding successful:", decoded_bits == input_bits)

if __name__ == "__main__":
    main()
