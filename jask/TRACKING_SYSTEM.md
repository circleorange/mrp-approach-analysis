# Enhanced Dual Tracking System

This document describes the enhanced dual tracking system for process reassignments and solution metrics.

## Files Generated

### 1. `process_reassignments.csv` (Algorithmic Analysis)
Tracks **all process reassignments** including exploration moves that are evaluated but not accepted. This file provides comprehensive insight into the search algorithm behavior.

**Purpose**: Understanding how the search algorithm explores the solution space
**Data Volume**: High (captures every move evaluation)
**Use Case**: Algorithm performance analysis, search behavior study

### 2. `accepted_reassignments.csv` (Solution Analysis)  
Tracks **only accepted reassignments** between solution states. This file shows the actual evolution path of the solution.

**Purpose**: Understanding how the solution evolves during optimization
**Data Volume**: Low (captures only accepted moves that change the solution state)
**Use Case**: Solution evolution analysis, cost improvement tracking

**Columns for Both Files:**
- `MoveNum`: Sequential move number within each file
- `ProcessID`: ID of the process being moved
- `SourceMachine`: Source machine ID
- `DestMachine`: Destination machine ID
- `OriginalMachine`: Original machine ID from initial solution
- `Service`: Service ID of the process
- `MoveCost`: Cost of moving this process
- `ProcessResourceRequirements`: Array of resource requirements
- `Improvement`: Percentage improvement of this move
- `Timestamp`: When the move occurred
- `SolutionId`: Current solution ID
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

### 3. `solution_states.csv`
Enhanced with additional solution-level metrics:

**New Columns Added:**
- `LoadCost`: Load cost component
- `BalanceCost`: Balance cost component  
- `MachineMoveCost`: Machine move cost component
- `ProcessMoveCost`: Process move cost component
- `ServiceMoveCost`: Service move cost component
- `NumConstraintsUnsatisfied`: Total number of unsatisfied constraints
- `IsFeasible`: Boolean indicating if solution is feasible

### 4. `machine_metrics.csv` (New File)
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

## Dual Tracking Comparison

| Aspect | process_reassignments.csv | accepted_reassignments.csv |
|--------|---------------------------|----------------------------|
| **Purpose** | Algorithmic analysis | Solution evolution analysis |
| **Moves Tracked** | All exploration moves | Only accepted moves |
| **Data Volume** | High (~355 moves) | Low (~1 accepted move) |
| **Research Use** | Search behavior study | Solution progression tracking |
| **Comparison** | Similar to JASK original behavior | Similar to MEHTA tracking approach |

## Usage

### Automatic Tracking
- Process reassignment tracking happens automatically on each move exploration
- Accepted reassignment tracking happens only when moves are accepted by the hill climber
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

The enhanced dual tracking enables analysis of:

1. **Algorithm Efficiency** - Compare exploration vs accepted move ratios
2. **Search Behavior** - How many moves are evaluated vs accepted
3. **Solution Evolution** - Track actual solution improvement path
4. **Resource utilization patterns** - How machine resources are used over time
5. **Load balancing effectiveness** - Distribution of processes across machines
6. **Constraint satisfaction dynamics** - How feasibility changes during optimization
7. **Cost component evolution** - How different cost components change
8. **Machine efficiency** - Capacity utilization and constraint satisfaction per machine

## Cross-Algorithm Compatibility

This dual tracking system now provides compatibility with different tracking philosophies:

- **JASK J12**: Provides both exploration-based tracking (like original JASK) and solution-based tracking (like MEHTA)
- **MEHTA CB-LNS**: Uses accepted-solution tracking approach (equivalent to accepted_reassignments.csv)
- **GAVRA S41**: Uses accepted-solution tracking approach with dual search tracking

## File Locations

All tracking files are generated in the working directory where the application runs.
