# Bit-by-Bit-Hackathon
## Challenge 1: Side-Channel Shenanigans: The RSA Key Recovery Challenge 🕵️‍♂️
This challenge focuses on recovering a secret RSA private key from a microcontroller by analyzing its power consumption during decryption. The target is a custom 16-bit RSA crypto-module running on an STM32F303 microcontroller.

### Mission
The primary objective is to recover the secret 15-bit RSA private key, 

The process involves:

Establishing Communication: Write a Python script to communicate with the target device.

Gathering Traces: Send random 2-byte ciphertexts (which must be integers less than the modulus N, 64507) to the device and capture the corresponding power traces during decryption.

Key Recovery: Analyze the collected power traces to reconstruct the private key.

### Key Details & Verification
The private key 
d is 15 bits long.

The Most Significant Bit (MSB) is known to be 
1.
The 4 Least Significant Bits (LSBs) are known to be 
0001.

The final key structure is 

1??????????0001, leaving only 10 bits to be recovered.

Verification: To confirm the correct key has been found, you send the recovered key d to the device as a ciphertext input. If the device returns the plaintext value 

6267, the mission is successful.

---

## Challenge 2: ModelSpy: Identify the CNN model from Side-Channel CPU Traces 🧠
This challenge is set in a cloud computing environment where multiple users share CPU resources. The goal is to identify which Convolutional Neural Network (CNN) model a co-tenant is running by observing CPU performance counters from your own partition.

### Scenario
You can observe system-level telemetry (like cache misses and instruction cycles) using tools like Linux 

perf. The patterns in this data can act as "side-channel fingerprints" that are unique to specific workloads, such as a CNN inference run.

### Objective
Your task is to build a classification algorithm that can analyze unlabelled 

perf traces from a shared CPU and identify which of the following CNN models is being run by another user:

Resnet , AlexNet, VGG , DenseNet , Inception_V3 , MobileNet_V2 , ShuffleNet_V2 

You are provided with a small set of labeled traces for these models to train your algorithm.

### Evaluation
Solutions are judged on several criteria:

Primary (60%): Classification accuracy on a hidden set of evaluation traces.

Secondary (40%): Explainability of the model, its runtime efficiency, and the clarity of the final report.

---
## Challenge 3: Side-Channel Key Recovery with Neural Networks 🤖
This challenge addresses a scenario where standard side-channel attacks like CPA fail because only a very limited number of power traces can be collected from the target device (Device A).

### The Problem
You must recover the first byte of an AES secret key from 

Device A. You only have a small number of traces 
(Na) from this device, which is insufficient for a standard CPA attack. To overcome this, you have access to 
Device B, a clone of Device A that is under your full control.

### Methodology: A Profiled Attack
The attack is performed in two steps:

###Training Phase (on Device B)

A large number of traces (Np) are collected from Device B, for which the plaintext, ciphertext, and a known key are available.

This large, labeled dataset is used to train a neural network. The network learns to predict the probability distribution of an intermediate sensitive variable, 
Z, from a given power trace.
A common choice for 
Z is the Hamming Weight of the S-box output: Z=HW(Sbox(P⊕K)).

### Key Recovery Phase (on Device A)

The trained model is applied to the few traces collected from Device A.

For each of the 256 possible key bytes, a 

log-likelihood score is calculated by aggregating the model's predictions across all of Device A's traces.

The key candidates are then ranked by their score, with the highest score indicating the most likely key byte.


