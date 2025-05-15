# decoder.py

import numpy as np

def viterbi_decode(encoded_bits):
    """
    Decodes convolutional encoded bits using the Viterbi algorithm.
    Assumes rate 1/2 and constraint length 3 with G1 = 0b111, G2 = 0b101.
    """
    n = 2  # number of output bits per input bit
    k = 3  # constraint length
    num_states = 2 ** (k - 1)
    
    # Define the state transition table and output for each input (0 or 1)
    next_state = {}
    output = {}
    for state in range(num_states):
        for bit in [0, 1]:
            new_state = ((state << 1) | bit) & (num_states - 1)
            out1 = parity((bit & 1) + ((state >> 0) & 1) + ((state >> 1) & 1))  # G1 = 111
            out2 = parity((bit & 1) + ((state >> 1) & 1))                      # G2 = 101
            next_state[(state, bit)] = new_state
            output[(state, bit)] = (out1, out2)

    # Initialize path metrics and paths
    path_metrics = np.full((len(encoded_bits)//n + 1, num_states), np.inf)
    paths = np.full((len(encoded_bits)//n + 1, num_states), -1, dtype=int)
    path_metrics[0][0] = 0

    # Forward pass: compute path metrics
    for t in range(0, len(encoded_bits), n):
        received = tuple(encoded_bits[t:t+n])
        for state in range(num_states):
            if path_metrics[t//n][state] < np.inf:
                for bit in [0, 1]:
                    ns = next_state[(state, bit)]
                    expected = output[(state, bit)]
                    dist = hamming_distance(expected, received)
                    metric = path_metrics[t//n][state] + dist
                    if metric < path_metrics[t//n + 1][ns]:
                        path_metrics[t//n + 1][ns] = metric
                        paths[t//n + 1][ns] = state * 2 + bit

    # Backtrace to find best path
    decoded = []
    state = np.argmin(path_metrics[-1])
    for t in range(len(paths) - 1, 0, -1):
        prev = paths[t][state]
        decoded_bit = prev & 1
        decoded.insert(0, decoded_bit)
        state = prev >> 1

    return decoded

def parity(x):
    return x % 2

def hamming_distance(a, b):
    return sum(x != y for x, y in zip(a, b))
