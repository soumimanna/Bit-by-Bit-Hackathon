# Bit-by-Bit-Hackathon
# 🔐 Side-Channel Attack: RSA Key Recovery Challenge

This repository contains our solution for **The Side Channel Hackathon 2025 – Problem 1**:  
Recovering a 15-bit RSA private key from side-channel leakage on a ChipWhisperer target device.
---

# 📖 Problem Statement
A vulnerable RSA decryption implementation on an STM32F303 (CW308 target) leaks information via **power consumption**.  
The goal is to:
1. Capture power traces while the device decrypts ciphertexts.
2. Use side-channel analysis (Square-and-Multiply leakage) to recover the private key d.
3. Verify the recovered key by sending it to the device (correct output = 6267).
---
## Usage
1. Capture Power Traces
Make sure the board is flashed with simpleserial_rsa-CW308_STM32F3.hex.
--
## Requirements
### Hardware
[ChipWhisperer-Lite](https://rtfm.newae.com/ChipWhisperer-Lite/)
CW308 UFO board with STM32F303 target
USB connection to host machine (Linux/WSL with usbipd-win if on Windows)

### Software
Python 3.8+
numpy, matplotlib
scipy optional (recommended for filtering / medfilt — code falls back if missing)
For hardware capture (main.py) you need the corresponding capture library (e.g. ChipWhisperer) and the target firmware (e.g. simpleserial_rsa-CW308_STM32F3.hex). 
Install core Python packages:

pip install numpy matplotlib scipy
# plus chipwhisperer or your capture library if required
---
## Given Bits and attack hints
Use these constraints to reduce search space and increase reliability:
Key length: d is 15 bits long.
Known bits:

MSB = 1
4 LSBs = 0001
Key pattern (known + unknown):

1 ? ? ? ? ? ? ? ? ? ? 0 0 0 1
Only the 10 middle bits are unknown — fix MSB and LSBs in your hypothesis simulation to reduce ambiguity.

---

2. Recover the Private Key
Run:
python3 recover_key.py
This script:


Splits each trace into 15 windows (1 per key bit).


Detects extra multiplications (bit=1) vs only squaring (bit=0).
Reconstructs the 15-bit key, using known hints:
MSB = 1
4 LSBs = 0001




This sends the recovered key d as ciphertext.

If the firmware returns plaintext 6267, the attack succeeded ✅.
