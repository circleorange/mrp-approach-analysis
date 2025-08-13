# Machine Reassignment Problem - Analysis of Approaches

This repository contains three different implementations of solutions to the ROADEF/EURO 2012 Machine Reassignment Problem, each enhanced with detailed process reassignment tracking capabilities for comparative analysis.

## Repository Structure

### 📊 **JASK (Java - Team J12)**
- **Language**: Java with CPLEX integration
- **Algorithm**: Mixed Integer Programming with heuristic optimization  
- **Status**: ✅ Tracking implemented
- **Tracking**: Records reassignments during solution optimization
- **Key Features**: CPLEX-based solver, comprehensive constraint handling

### 🔧 **GAVRA (C++ - Team S41)**  
- **Language**: C++
- **Algorithm**: Dual solution local search with weight modifications
- **Status**: ✅ Tracking implemented (with cost normalization fix)
- **Tracking**: Records reassignments with original cost weights
- **Key Features**: Parallel dual solutions, dynamic weight adjustments

### 🧠 **MEHTA (C++ - Constraint-Based Large Neighborhood Search)**
- **Language**: C++  
- **Algorithm**: CB-LNS (Constraint-Based Large Neighborhood Search)
- **Status**: ✅ Tracking implemented and integrated
- **Tracking**: CSV tracking of accepted solution transitions during CB-LNS search
- **Key Features**: LNS with constraint-based selection, clean solution progression tracking
- **Performance**: Captures accepted moves only (15 moves vs millions of exploration moves)

## Analysis Capabilities

With tracking implemented across all repositories, this enables:
- **Cross-algorithm comparison** of optimization strategies
- **Process mobility analysis** across different approaches  
- **Cost evolution patterns** during solution search
- **Resource utilization efficiency** comparison
- **Algorithm performance benchmarking**

## Implementation Status Summary

| Repository | Algorithm | Tracking Status | Integration | CSV Output |
|------------|-----------|-----------------|-------------|------------|
| JASK       | MIP/CPLEX | ✅ Complete | ✅ Integrated | ✅ Working |
| GAVRA      | Dual Search | ✅ Complete | ✅ Integrated | ✅ Working |
| MEHTA      | CB-LNS    | ✅ Complete | ✅ Integrated | ✅ Working |

**Note**: All three implementations now have fully functional tracking systems that capture process reassignments during optimization, enabling comprehensive cross-algorithm analysis.

## Tracking Data Format

All implementations generate CSV tracking files. GAVRA and JASK use the full 22-column format:
- MoveNum, ProcessID, SourceMachine, DestMachine, OriginalMachine
- Service, MoveCost, ProcessResourceRequirements, Improvement, Timestamp
- SolutionId, Machine resource usage/capacities, Process counts
- LoadCost, BalanceCost, SolutionCost

MEHTA currently uses an enhanced 8-column format for accepted solution transitions:
- moveNumber, processId, sourceMachine, destMachine, moveCost, improvement, timestamp, solutionId, solutionCost

## Usage

Each subdirectory contains specific build and execution instructions. Use the same dataset files (from `jask/data/`) for consistent comparison across all three implementations.

---
*Last updated: August 2025*
