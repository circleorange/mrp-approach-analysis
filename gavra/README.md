# S41 Algorithm Analysis Setup

This repository contains the modified S41 team solution from the ROADEF 2012 Machine Reassignment Problem challenge, enhanced with detailed tracking and analysis capabilities.

## Overview

The S41 algorithm is a C++ implementation that uses dual solution approach with local search methods. This modified version adds comprehensive tracking of process reassignments, machine utilization, and cost evolution during the optimization process.

## Dependencies

- GCC C++ compiler with C++11 support
- Make
- Python 3.x with the following packages for analysis:
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - jupyter

## Build

To compile the solver:

```bash
cd gavra/Releasegcc
make clean
make
```

This creates the `machineReassignment` executable.

## Usage

### Basic Usage

```bash
cd gavra/Releasegcc
./machineReassignment -p <model_file> -i <initial_assignment> -o <output_file> -t <time_limit> -s <seed>
```

### Parameters

- `-p <file>`: Instance data file
- `-i <file>`: Initial assignment file  
- `-o <file>`: Output solution file
- `-t <seconds>`: Time limit in seconds
- `-s <seed>`: Random seed for deterministic runs
- `-name`: Display team name (S41)

### Using the Analysis Script

For convenient analysis runs:

```bash
./run_analysis.sh [dataset] [time_limit] [seed]
```

Example:
```bash
./run_analysis.sh a1_2 60 12345
```

This will:
1. Run the algorithm on the specified dataset
2. Generate tracking files with detailed reassignment data
3. Create a timestamped results directory
4. Provide instructions for analysis

## Tracking Output

The modified algorithm generates two CSV files:
- `process_reassignments_sol1.csv`: Tracking data for solution 1
- `process_reassignments_sol2.csv`: Tracking data for solution 2

Each file contains the following columns:
- `MoveNum`: Sequential move number
- `ProcessID`: ID of the process being moved
- `SourceMachine`: Source machine ID
- `DestMachine`: Destination machine ID  
- `OriginalMachine`: Original machine ID of the process
- `Service`: Service ID of the process
- `MoveCost`: Cost of moving this process
- `ProcessResourceRequirements`: Resource requirements array [R1,R2,R3,R4]
- `Improvement`: Cost improvement from this move
- `Timestamp`: Timestamp of the move
- `SolutionId`: Solution ID counter
- `SourceMachineResourceUsage`: Resource usage on source machine
- `DestMachineResourceUsage`: Resource usage on destination machine
- `SourceMachineCapacities`: Capacity limits on source machine
- `DestMachineCapacities`: Capacity limits on destination machine
- `SourceMachineTransientUsage`: Transient resource usage on source machine
- `DestMachineTransientUsage`: Transient resource usage on destination machine
- `SourceMachineProcessCount`: Number of processes on source machine
- `DestMachineProcessCount`: Number of processes on destination machine
- `LoadCost`: Current load cost
- `BalanceCost`: Current balance cost
- `SolutionCost`: Total solution cost

## Analysis

Use the provided Jupyter notebook for analysis:

```bash
cd gavra/analytics
jupyter notebook analysis.ipynb
```

The notebook provides:
- Cost evolution visualization
- Process mobility analysis
- Machine utilization patterns
- Comparison between dual solutions
- Summary statistics

## Algorithm Characteristics

The S41 algorithm uses:
- Dual solution approach (two parallel searches with different parameters)
- Local search with shift and swap operations
- Preprocessing to handle constrained processes
- Adaptive parameters based on instance size
- Big process rearrangement techniques

### Instance-Specific Parameters

- **A instances** (≤100K processes × machines): Higher iteration counts, more ranges
- **B instances** (>100K processes × machines): Reduced iterations, fewer ranges for efficiency

## Integration with Existing Analysis Tools

The tracking format is compatible with existing analysis tools from the Java implementation:

```bash
# Copy tracking files to Java project for analysis
cp gavra/results_*/process_reassignments_sol*.csv /home/pbiel/repos/mrp/jask/
```

## Files Added/Modified

### Original Files (Modified)
- `src/solution.h`: Added tracking method declarations
- `src/solution.cpp`: Implemented tracking functionality
- `src/machine_resource.h`: Added usage getter methods
- `src/solverGoogle.cpp`: Added tracking initialization and cleanup

### New Files
- `analytics/analysis.ipynb`: Analysis notebook
- `run_analysis.sh`: Convenient analysis runner script
- `README.md`: This documentation

## Performance Notes

- The tracking adds minimal overhead to the algorithm
- Generated CSV files can be large (100MB+ for longer runs)
- The dual solution approach typically generates 2× the tracking data
- For very large instances, consider shorter time limits for initial analysis

## Comparison with Java Implementation

Both implementations now provide compatible tracking data, enabling:
- Direct algorithm comparison
- Performance benchmarking  
- Different approach analysis (local search vs. other methods)
- Cross-validation of results

The C++ S41 implementation generally shows:
- High-frequency local search moves
- Dual solution convergence patterns
- Significant cost improvements through iterative refinement

# Example

- Compile the project:
```
cd /home/pbiel/repos/mrp/gavra/Releasegcc && make clean && make
```
- Short test run:
```
./machineReassignment -p /home/pbiel/repos/mrp/jask/data/A/model_a1_2.txt -i /home/pbiel/repos/mrp/jask/data/A/assignment_a1_2.txt -o test_output2.txt -t 10 -s 12345
```
- or, use conventient wrapper script to run the algorithm with different parameters and datasets:
```
./run_analysis.sh a1_2 15 42
```
- Run final summary script to help with analysis:
```
python3 quick_analysis.py results_a1_2_20250804_180242
```
