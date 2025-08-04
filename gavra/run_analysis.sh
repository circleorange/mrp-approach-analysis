#!/bin/bash

# S41 Algorithm Runner Script
# Usage: ./run_analysis.sh [dataset] [time_limit] [seed]

# Default parameters
DATASET=${1:-"a1_2"}
TIME_LIMIT=${2:-30}
SEED=${3:-42}

# Paths
GAVRA_DIR="/home/pbiel/repos/mrp/gavra"
DATA_DIR="/home/pbiel/repos/mrp/jask/data/A"
EXECUTABLE="$GAVRA_DIR/Releasegcc/machineReassignment"

# Check if dataset files exist
MODEL_FILE="$DATA_DIR/model_${DATASET}.txt"
ASSIGNMENT_FILE="$DATA_DIR/assignment_${DATASET}.txt"

if [ ! -f "$MODEL_FILE" ]; then
    echo "Error: Model file not found: $MODEL_FILE"
    exit 1
fi

if [ ! -f "$ASSIGNMENT_FILE" ]; then
    echo "Error: Assignment file not found: $ASSIGNMENT_FILE"
    exit 1
fi

echo "Running S41 algorithm analysis..."
echo "Dataset: $DATASET"
echo "Time limit: $TIME_LIMIT seconds"
echo "Seed: $SEED"
echo "Model file: $MODEL_FILE"
echo "Assignment file: $ASSIGNMENT_FILE"
echo ""

# Create output directory with timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_DIR="$GAVRA_DIR/results_${DATASET}_${TIMESTAMP}"
mkdir -p "$OUTPUT_DIR"

# Run the algorithm
cd "$GAVRA_DIR/Releasegcc"

echo "Starting algorithm execution..."
./machineReassignment -p "$MODEL_FILE" -i "$ASSIGNMENT_FILE" -o "$OUTPUT_DIR/solution_${DATASET}.txt" -t "$TIME_LIMIT" -s "$SEED"

# Copy tracking files
if [ -f "process_reassignments_sol1.csv" ]; then
    mv process_reassignments_sol1.csv "$OUTPUT_DIR/"
    echo "Moved solution 1 tracking data to $OUTPUT_DIR/"
fi

if [ -f "process_reassignments_sol2.csv" ]; then
    mv process_reassignments_sol2.csv "$OUTPUT_DIR/"
    echo "Moved solution 2 tracking data to $OUTPUT_DIR/"
fi

# Copy output solution
if [ -f "$OUTPUT_DIR/solution_${DATASET}.txt" ]; then
    echo "Solution saved to $OUTPUT_DIR/solution_${DATASET}.txt"
fi

echo ""
echo "Analysis complete. Results saved to: $OUTPUT_DIR"
echo ""
echo "To analyze the results, run:"
echo "  cd $OUTPUT_DIR"
echo "  jupyter notebook ../analytics/analysis.ipynb"
echo ""
echo "Or copy the tracking files to analyze with existing tools:"
echo "  cp $OUTPUT_DIR/process_reassignments_sol*.csv /home/pbiel/repos/mrp/jask/"
