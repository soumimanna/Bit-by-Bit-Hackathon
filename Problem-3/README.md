# Side-Channel Key Recovery with Neural Networks 🧠
This repository contains a solution for a side-channel attack challenge, demonstrating how to recover an AES encryption key byte using a neural network. The attack is effective even when only a limited number of power traces are available from the target device. This is achieved by training a model on a separate, identical "clone" device.

The Challenge: Profiled Side-Channel Attack
In many real-world scenarios, it's difficult to collect a large number of power consumption traces from a target device (let's call it Device A). This scarcity of data makes standard side-channel attacks like Correlation Power Analysis (CPA) ineffective.


This project tackles a scenario where we have:

Device A (Target): The device whose secret key we want to find. We can only collect a small number of power traces from it.

Device B (Clone): An identical device that is fully under our control. We can set its key and collect a large number of traces, creating a rich dataset for training.

The goal is to leverage the data from Device B to build a powerful model that can then successfully attack Device A.

---

# Methodology 🛠️
The attack is performed in two main steps: a 

training phase using the clone device and a key recovery phase on the target device.

## 1. Training Phase on Device B
The first step is to train a neural network to recognize patterns in the power traces.

Dataset: We use the large dataset from Device B, which includes power traces, corresponding plaintexts, and the known secret keys.

The Model's Goal: The network is trained to predict an intermediate sensitive value from a given power trace. In this implementation, the sensitive value 

Z is the Hamming Weight (HW) of the AES S-box output. The Hamming Weight is simply the number of '1's in the binary representation of a number.

## The label for each trace t is calculated as:

 Z=HW(Sbox(P⊕K))

where P is the plaintext byte and K is the key byte.

Output: The trained model takes a power trace as input and outputs a probability distribution over the 9 possible Hamming Weight values (0 through 8).


## 2. Key Recovery Phase on Device A
With the trained model, we can now attack the target device.

Prediction: The model is applied to each of the few traces collected from Device A. For each trace, it produces a vector of probabilities for the 9 possible Hamming Weight values.

Key Ranking: To find the most likely key, we iterate through all 256 possible key bytes (k from 0 to 255). For each key guess, we calculate a 

log-likelihood score by aggregating the results across all of Device A's traces.

---

# Result: The key guess with the highest log-likelihood score is the most probable secret key.

Implementation Details
The solution is implemented in Python using the TensorFlow and Keras libraries.

Dependencies
numpy

tensorflow

You can install them using pip:

---
## Bash:

pip install numpy tensorflow
Neural Network Architecture
A simple Multi-Layer Perceptron (MLP) is used for this task. The architecture is as follows:

Input Layer: Takes a flattened power trace vector.

Hidden Layer 1: A Dense layer with 64 neurons and ReLU activation.

Hidden Layer 2: A Dense layer with 64 neurons and ReLU activation.

Output Layer: A Dense layer with 9 neurons (one for each possible Hamming Weight) and Softmax activation to produce a probability distribution.

The model is compiled with the Adam optimizer and categorical cross-entropy loss function.

---
# How to Run the Attack 🚀
Clone the Repository:

Bash

git clone <repository-url>
cd <repository-directory>
Organize Datasets: Place the dataset files into the following directory structure:

.
├── datasetA/
│   ├── plaintext.npy
│   └── trace.npy
├── datasetB/
│   ├── key.npy
│   ├── plaintext.npy
│   └── trace.npy
└── cw_template.py
Execute the Script: Run the python script to start the training and attack process.

Bash

python cw_template.py
The script will first train the model using datasetB, save it as trained_sca_model.h5, and then use it to perform the key recovery attack on datasetA.

---
# Results 📊
The script will output a sorted list of all 256 possible key bytes, ranked from most likely to least likely. It will also display the top 5 most probable keys with their corresponding log-likelihood scores.

An example of the final output looks like this:

--- Attack Results ---
✅ Key recovery complete. Displaying the most likely keys.
Sorted list of possible keys (most likely first):
['0x2f', '0x1a', '0x9c', '0x7e', '0x4a', ... ]
Top 5 most likely key bytes:
  Rank 1: Key = 0x2f (Log-Likelihood: -198.45)
  Rank 2: Key = 0x1a (Log-Likelihood: -235.12)
  Rank 3: Key = 0x9c (Log-Likelihood: -240.78)
  Rank 4: Key = 0x7e (Log-Likelihood: -244.31)
  Rank 5: Key = 0x4a (Log-Likelihood: -248.99)
