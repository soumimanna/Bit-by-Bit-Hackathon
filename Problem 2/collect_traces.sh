#!/bin/bash

# --- Configuration ---
# List of all candidate CNN models to profile. [cite: 16]
MODELS=(
    "Resnet"
    "AlexNet"
    "VGG"
    "DenseNet"
    "Inception_V3"
    "MobileNet_V2"
    "ShuffleNet_V2"
)

# List of perf events to capture for each model.
EVENTS=(
    "cycles"
    "instructions"
    "cache-misses"
    "branch-instructions"
    "branch-misses"
)

# Number of times to run the collection for each model/event pair.
NUM_RUNS=5

# Base directory to save all our collected traces.
OUTPUT_DIR="my_collected_traces2"

# --- Script Logic ---
echo "Starting trace acquisition..."
mkdir -p $OUTPUT_DIR

# Outer loop: Iterate over each CNN model.
for model in "${MODELS[@]}"; do
    echo "--- Profiling Model: $model ---"
    
    # Create a subdirectory for the current model's traces.
    mkdir -p "$OUTPUT_DIR/$model"

    # Inner loop: Iterate over each perf event.
    for event in "${EVENTS[@]}"; do
        echo "  Collecting event: $event"

        # Innermost loop: Run multiple times for robustness.
        for (( run=1; run<=$NUM_RUNS; run++ )); do
            echo "    - Run $run of $NUM_RUNS"
            
            # Define the output file path.
            OUTPUT_FILE="$OUTPUT_DIR/$model/${event}_run${run}.txt"

            # --- OPTIMIZED COMMAND ---
            # Use 'timeout' to limit the collection to 10 seconds for each run.
            timeout 10s perf stat -I 50 -e "$event" \
                /home/hackathon/dist/model_inference "$model" \
                2> "$OUTPUT_FILE"
        done
    done
done

echo "--- Trace acquisition complete! ---"
echo "Data saved in the '$OUTPUT_DIR' directory."
































# #!/bin/bash

# # --- Configuration ---
# # List of all candidate CNN models to profile.
# MODELS=(
#     "Resnet"
#     "AlexNet"
#     "VGG"
#     "DenseNet"
#     "Inception_V3"
#     "MobileNet_V2"
#     "ShuffleNet_V2"
# )

# # List of perf events to capture for each model.
# EVENTS=(
#     "cycles"
#     "instructions"
#     "cache-misses"
#     # "L1-dcache-load-misses"
#     "branch-instructions"
#     "branch-misses"
# )

# # Number of times to run the collection for each model/event pair.
# NUM_RUNS=5

# # Base directory to save all our collected traces.
# OUTPUT_DIR="my_collected_traces"

# # --- Script Logic ---
# echo "Starting trace acquisition..."
# mkdir -p $OUTPUT_DIR

# # Outer loop: Iterate over each CNN model.
# for model in "${MODELS[@]}"; do
#     echo "--- Profiling Model: $model ---"
    
#     # Create a subdirectory for the current model's traces.
#     mkdir -p "$OUTPUT_DIR/$model"

#     # Inner loop: Iterate over each perf event.
#     for event in "${EVENTS[@]}"; do
#         echo "  Collecting event: $event"

#         # Innermost loop: Run multiple times for robustness.
#         for (( run=1; run<=$NUM_RUNS; run++ )); do
#             echo "    - Run $run of $NUM_RUNS"
            
#             # Define the output file path.
#             OUTPUT_FILE="$OUTPUT_DIR/$model/${event}_run${run}.txt"

#             # Construct and execute the perf command.
#             # We assume the model_inference program takes the model name as an argument.
#             # The output of perf stat (stderr) is redirected to our file.
#             perf stat -I 50 -e "$event" \
#                 /home/hackathon/dist/model_inference "$model" \
#                 2> "$OUTPUT_FILE"
#         done
#     done
# done

# echo "--- Trace acquisition complete! ---"
# echo "Data saved in the '$OUTPUT_DIR' directory."