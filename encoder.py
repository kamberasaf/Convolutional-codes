# encoder.py

def encode(input_bits):
    """
    Rate 1/2 convolutional encoder with constraint length 3.
    Generator polynomials: G1 = (1,1,1), G2 = (1,0,1)

    Args:
        input_bits (list of int): binary input sequence, e.g., [1, 0, 1, 1]

    Returns:
        list of int: encoded bit stream
    """
    g1 = [1, 1, 1]  # generator polynomial for output 1
    g2 = [1, 0, 1]  # generator polynomial for output 2

    # zero padding for tail bits (flush the shift register)
    input_bits = input_bits + [0, 0]
    encoded_bits = []

    for i in range(len(input_bits) - 2):
        window = input_bits[i:i+3]
        output_bit1 = sum([a*b for a, b in zip(window, g1)]) % 2
        output_bit2 = sum([a*b for a, b in zip(window, g2)]) % 2
        encoded_bits.extend([output_bit1, output_bit2])

    return encoded_bits
