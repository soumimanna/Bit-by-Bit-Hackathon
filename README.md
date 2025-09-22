# Bit-by-Bit-Hackathon
# 🔐 RSA Side-Channel Attack – Hackathon 2025

This repository contains my work for Hackathon Challenge 1: Side-Channel Shenanigans – The RSA Key Recovery Challenge (from Bit-by-Bit: The Side Channel Hackathon 2025).

The challenge involves performing power side-channel analysis (SCA) on a lightweight 16-bit RSA crypto-module implemented on an STM32F3 target board, using the ChipWhisperer-Lite platform.

# 📜 Challenge Description

From the problem statement:

The target is an STM32F303 running RSA decryption firmware.

Power traces are captured using ChipWhisperer-Lite during decryption operations.

The implementation uses the Square-and-Multiply algorithm, which leaks key information.

The secret RSA private key d is 15 bits long with known format:

1??????????0001


# Objective:

Capture traces while the device performs RSA decryption.

Analyze traces to distinguish between square and multiply operations.

Recover the missing 10 bits of the private key d.

Verify the recovered key: when sent as input ciphertext, the module must return plaintext 6267.

# 📂 Repository Contents

rsa_trace.ipynb → Jupyter Notebook for:

Programming the target with RSA firmware

Capturing power traces using ChipWhisperer

Storing ciphertext–trace pairs for later analysis

Example trace visualization

Hackathon_2025_problem1.pdf → Official problem statement and rules.

# 🚀 Workflow

## Setup

Hardware: CW308 + STM32F303 + ChipWhisperer-Lite

Firmware: simpleserial_rsa-CW308_STM32F3.hex

Trace Acquisition

Send random ciphertexts c < N (64507)

Capture ~500–5000 traces

Save traces (.npy or .csv) with corresponding ciphertexts

## Analysis

Apply side-channel techniques (Differential Power Analysis / Template Matching)

Exploit leakage from conditional multiply in Square-and-Multiply

Reconstruct private key d bit by bit

## Verification

Send recovered d as input ciphertext

If response = 6267, key recovery successful 🎉

# 📊 Example Output

Sample captured trace waveform (from rsa_trace.ipynb):

Triggered on decryption start

Distinct patterns for square vs square+multiply

Recovered key format:

d = 1??????????0001


(Final key revealed in report after analysis step)

# 🛠️ Tools & Libraries

ChipWhisperer

Python 3.8+

NumPy, Pandas, Matplotlib

# 📑 Submission Requirements

Jupyter Notebook with working code (rsa_trace.ipynb)

Problem Statement (Hackathon_2025_problem1.pdf)

Final Report (to be added) with recovered 15-bit RSA private key

# 📌 Status

✔️ Trace acquisition implemented
✔️ Basic analysis prepared
⏳ Final key recovery & verification ongoing
