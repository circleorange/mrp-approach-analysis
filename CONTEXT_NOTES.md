# Machine Reassignment Problem - Context Notes

## Project Overview
This repository contains three algorithm implementations for the ROADEF/EURO 2012 Machine Reassignment Problem, each with tracking capabilities for comparative analysis:

### Algorithms
- **JASK (Java - J12 Team)**: MIP with CPLEX, dual tracking system
- **GAVRA (C++ - S41 Team)**: Dual solution local search, currently tracks accepted transitions only  
- **MEHTA (C++ - CB-LNS)**: Constraint-based large neighborhood search

### Dataset Focus
- **Only Dataset A** is relevant (`solveAFinal` method)
- Uses `a1_1`, `a1_2`, `a1_4` problem instances
- Test instances available in `/home/pbiel/repos/mrp/jask/data/A/`

## Current Tracking Implementation (GAVRA)

### Current State
GAVRA currently implements **accepted solution transition tracking** only:
- Tracks reassignments when algorithm moves from one accepted solution to another
- Files: `accepted_reassignments_sol1.csv`, `accepted_reassignments_sol2.csv`
- Infrastructure exists for exploration tracking but not fully activated

### Implementation Location
- **Core tracking**: `gavra/src/solution.h` and `gavra/src/solution.cpp`
- **Integration**: `gavra/src/testovi.cpp` (`solveAFinal` method)
- **Dual solution handling**: Two separate tracking files for parallel solutions

## Required Changes

### Goal
Implement dual tracking output:
1. **Global reassignments file**: Track ALL reassignments during search (including exploration moves)
2. **Accepted reassignments file**: Keep current behavior (accepted solution transitions only)

### Expected Files After Changes
- `process_reassignments_sol1.csv` - ALL reassignments (global tracking)
- `process_reassignments_sol2.csv` - ALL reassignments (global tracking)  
- `accepted_reassignments_sol1.csv` - Accepted transitions only (current behavior)
- `accepted_reassignments_sol2.csv` - Accepted transitions only (current behavior)

## Build & Test Commands

```bash
# Build GAVRA
cd /home/pbiel/repos/mrp/gavra/Releasegcc && make clean && make

# Quick test
./machineReassignment -p /home/pbiel/repos/mrp/jask/data/A/model_a1_4.txt -i /home/pbiel/repos/mrp/jask/data/A/assignment_a1_4.txt -o test_output.txt -t 10 -s 12345

# Verify tracking files
ls -la *.csv
wc -l *.csv
```

## Key Technical Details

### Current Tracking Flow
1. `solveAFinal` calls dual solution optimization
2. Only "accepted solution transitions" are tracked (between algorithm-accepted states)
3. Individual process reassignments during local search are NOT tracked globally

### Required Integration Points
- **Local search functions**: Need to add global tracking to `local_search_shift`, `local_search_swap` etc.
- **Process reassignment**: Each `sol->reassignProcess()` call should be globally tracked
- **Dual tracking**: Maintain both global and accepted tracking simultaneously

### CSV Format
22-column format compatible with JASK for cross-algorithm analysis:
- MoveNum, ProcessID, SourceMachine, DestMachine, OriginalMachine, Service, MoveCost
- ProcessResourceRequirements, Improvement, Timestamp, SolutionId
- Machine resource usage, capacities, transient usage, process counts
- LoadCost, BalanceCost, SolutionCost
