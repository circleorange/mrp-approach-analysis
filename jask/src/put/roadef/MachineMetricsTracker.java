package put.roadef;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

/**
 * Utility class for tracking machine-level metrics during optimization
 */
public class MachineMetricsTracker {
    private static PrintWriter machineTracker = null;
    private static final Object trackingLock = new Object();
    private static long snapshotCounter = 0;
    
    /**
     * Initialize the machine metrics tracker
     * @param filename Name of the CSV file to write machine metrics to
     */
    public static void initializeMachineTracker(String filename) {
        synchronized (trackingLock) {
            if (machineTracker == null) {
                try {
                    machineTracker = new PrintWriter(new FileWriter(filename, false));
                    machineTracker.println("SnapshotId,Timestamp,SolutionId,MachineId," +
                        "TotalResourceUsage,TotalCapacity,TotalTransientUsage," +
                        "ProcessCount,LoadCostContribution,BalanceCostContribution," +
                        "CapacityUtilizationPercent,IsFeasible");
                    machineTracker.flush();
                } catch (IOException e) {
                    System.err.println("Error creating machine tracker: " + e.getMessage());
                }
            }
        }
    }
    
    /**
     * Take a snapshot of all machine metrics for the current solution
     * @param solution The solution to analyze
     * @param solutionId The ID of the current solution
     */
    public static void takeMachineSnapshot(SmartSolution solution, long solutionId) {
        if (machineTracker == null) {
            initializeMachineTracker("machine_metrics.csv");
        }
        
        synchronized (trackingLock) {
            if (machineTracker != null) {
                long timestamp = System.currentTimeMillis();
                long snapshotId = ++snapshotCounter;
                Problem problem = solution.getProblem();
                
                for (int m = 0; m < problem.getNumMachines(); m++) {
                    // Calculate total resource usage and capacity for this machine
                    long totalUsage = 0;
                    long totalCapacity = 0;
                    long totalTransientUsage = 0;
                    
                    for (int r = 0; r < problem.getNumResources(); r++) {
                        totalUsage += solution.getResourceUsage(m, r);
                        totalCapacity += problem.getMachine(m).capacities[r];
                        totalTransientUsage += solution.getTransientUsage(m, r);
                    }
                    
                    // Process count for this machine
                    int processCount = solution.processesInMachine[m].size();
                    
                    // Calculate utilization percentage
                    double utilizationPercent = totalCapacity > 0 ? 
                        (double) totalUsage / totalCapacity * 100.0 : 0.0;
                    
                    // Check if this machine satisfies constraints
                    boolean machineIsFeasible = problem.checkCapacityConstraint(solution, m) &&
                                              problem.checkTransientUsageConstraint(solution, m);
                    
                    // Write machine data
                    machineTracker.printf("%d,%d,%d,%d,%d,%d,%d,%d,0,0,%.2f,%s%n",
                        snapshotId,
                        timestamp,
                        solutionId,
                        m,
                        totalUsage,
                        totalCapacity,
                        totalTransientUsage,
                        processCount,
                        // Load and balance cost contributions would need more complex calculation
                        utilizationPercent,
                        machineIsFeasible
                    );
                }
                machineTracker.flush();
            }
        }
    }
    
    /**
     * Close the machine metrics tracker
     */
    public static void closeMachineTracker() {
        synchronized (trackingLock) {
            if (machineTracker != null) {
                machineTracker.close();
                machineTracker = null;
            }
        }
    }
}
