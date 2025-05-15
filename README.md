# Convolutional Codes (Encoder + Viterbi Decoder)

This project implements a basic convolutional encoder and its corresponding Viterbi decoder in Python. It's intended for educational purposes and demonstrates the core principles of error-correcting codes used in digital communication systems.

## Features

- 📡 Rate 1/2 convolutional encoder  
- 🧠 Viterbi decoder using Hamming distance  
- 🌐 Trellis visualization support  
- 🔍 Bit-level simulation and easy-to-read outputs  
- 🧪 Includes test cases  

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/kamberasaf/Convolutional-codes.git
cd Convolutional-codes
```

### 2. Run an example
```bash
python main.py --input 1011001
```

### Sample Output:
```plaintext
Encoded: [1, 1, 1, 0, 0, 0, 1, 1, ...]
Decoded: [1, 0, 1, 1, 0, 0, 1]
```
