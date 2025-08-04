# Enhanced Tracking System

This document describes the enhanced tracking system for process reassignments and solution metrics.

## Files Generated

### 1. `process_reassignments.csv`
Enhanced to include additional machine-level metrics for each reassignment:

**New Columns Added:**
- `SourceMachineResourceUsage`: Array of resource usage for source machine
- `DestMachineResourceUsage`: Array of resource usage for destination machine  
- `SourceMachineCapacities`: Array of capacities for source machine
- `DestMachineCapacities`: Array of capacities for destination machine
- `SourceMachineTransientUsage`: Array of transient usage for source machine
- `DestMachineTransientUsage`: Array of transient usage for destination machine
- `SourceMachineProcessCount`: Number of processes on source machine
- `DestMachineProcessCount`: Number of processes on destination machine
- `LoadCost`: Current solution load cost
- `BalanceCost`: Current solution balance cost
- `SolutionCost`: Total solution cost

### 2. `solution_states.csv`
Enhanced with additional solution-level metrics:

**New Columns Added:**
- `LoadCost`: Load cost component
- `BalanceCost`: Balance cost component  
- `MachineMoveCost`: Machine move cost component
- `ProcessMoveCost`: Process move cost component
- `ServiceMoveCost`: Service move cost component
- `NumConstraintsUnsatisfied`: Total number of unsatisfied constraints
- `IsFeasible`: Boolean indicating if solution is feasible

### 3. `machine_metrics.csv` (New File)
Detailed machine-level metrics snapshot capability:

**Columns:**
- `SnapshotId`: Unique ID for each snapshot
- `Timestamp`: When snapshot was taken
- `SolutionId`: Associated solution ID
- `MachineId`: Machine identifier
- `TotalResourceUsage`: Sum of all resource usage on machine
- `TotalCapacity`: Sum of all capacities on machine
- `TotalTransientUsage`: Sum of all transient usage on machine
- `ProcessCount`: Number of processes on machine
- `LoadCostContribution`: Machine's contribution to load cost (placeholder)
- `BalanceCostContribution`: Machine's contribution to balance cost (placeholder)
- `CapacityUtilizationPercent`: Percentage of capacity being used
- `IsFeasible`: Whether machine satisfies all constraints

## Usage

### Automatic Tracking
- Process reassignment tracking happens automatically on each move
- Solution state tracking happens when `trackSolutionStateChange()` is called
- All trackers are automatically closed when `SmartSolution.closeTracker()` is called

### Manual Machine Snapshots
To take a machine metrics snapshot:

```java
SmartSolution solution = ...; // your solution
long solutionId = SmartSolution.getCurrentSolutionId();
MachineMetricsTracker.takeMachineSnapshot(solution, solutionId);
```

### Analysis Capabilities

The enhanced tracking enables analysis of:

1. **Resource utilization patterns** - How machine resources are used over time
2. **Load balancing effectiveness** - Distribution of processes across machines
3. **Constraint satisfaction dynamics** - How feasibility changes during optimization
4. **Cost component evolution** - How different cost components change
5. **Machine efficiency** - Capacity utilization and constraint satisfaction per machine

## File Locations

All tracking files are generated in the working directory where the application runs.
