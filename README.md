# Convolutional Codes (Encoder + Viterbi Decoder)

This project implements a basic convolutional encoder and its corresponding Viterbi decoder in Python. It's ideal for understanding the core principles of error-correcting codes used in communication systems.

## Features

- Rate 1/2 convolutional encoder
- Viterbi decoder using Hamming distance
- Support for trellis visualization
- Bit-level simulation

## Usage

### Encoding and Decoding Example
```bash
python main.py --input 1011001

Output:
Encoded: [1, 1, 1, 0, 0, 0, 1, 1, ...]
Decoded: [1, 0, 1, 1, 0, 0, 1]
