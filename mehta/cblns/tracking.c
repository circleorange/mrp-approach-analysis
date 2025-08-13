/**************************************************************************************************
	TRACKING INFRASTRUCTURE FOR MACHINE REASSIGNMENT PROBLEM - IMPLEMENTATION
	
	Provides comprehensive tracking of process reassignments during CB-LNS optimization.
	Generates CSV files compatible with JASK and GAVRA tracking formats for analysis.
 **************************************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "definitions.h"
#include "cost.h"
#include "machine.h"
#include "tracking.h"

/* Local tracking variables initialization */
int trackingEnabled = 0;
int moveNumber = 0;
FILE *trackingFile = NULL;
char *trackingFilename = NULL;
time_t trackingStartTime;
usint *previousMachine = NULL; /* Track previous machine assignment for each process */

void initTracking(const char* filename) {
    int i;
    
    trackingFilename = (char*)malloc(strlen(filename) + 1);
    strcpy(trackingFilename, filename);
    
    trackingFile = fopen(trackingFilename, "w");
    if (trackingFile == NULL) {
        fprintf(stderr, "Error: Cannot open tracking file %s\n", trackingFilename);
        return;
    }
    
    /* Allocate memory for tracking previous machine assignments */
    previousMachine = (usint*)malloc(no_processes * sizeof(usint));
    if (previousMachine == NULL) {
        fprintf(stderr, "Error: Cannot allocate memory for tracking\n");
        fclose(trackingFile);
        return;
    }
    
    /* Initialize with current machine assignments */
    for (i = 0; i < no_processes; i++) {
        previousMachine[i] = NM[i];
    }
    
    trackingStartTime = time(NULL);
    moveNumber = 0;
    trackingEnabled = 1;
    
    writeTrackingHeader();
    
    printf("Tracking initialized: %s\n", trackingFilename);
}

void writeTrackingHeader(void) {
    if (trackingFile == NULL) return;
    
    fprintf(trackingFile, "MoveNum,ProcessID,SourceMachine,DestMachine,OriginalMachine,");
    fprintf(trackingFile, "Service,MoveCost,");
    
    /* Process resource requirements */
    fprintf(trackingFile, "ProcessR0,ProcessR1,ProcessR2,ProcessR3,ProcessR4,ProcessR5,ProcessR6,ProcessR7,");
    fprintf(trackingFile, "ProcessR8,ProcessR9,ProcessR10,ProcessR11,ProcessR12,ProcessR13,ProcessR14,ProcessR15,");
    fprintf(trackingFile, "ProcessR16,ProcessR17,ProcessR18,ProcessR19,");
    
    fprintf(trackingFile, "Improvement,Timestamp,SolutionId,");
    
    /* Machine resource usage and capacities */
    fprintf(trackingFile, "DestMachineUsage0,DestMachineUsage1,DestMachineUsage2,DestMachineUsage3,DestMachineUsage4,");
    fprintf(trackingFile, "DestMachineUsage5,DestMachineUsage6,DestMachineUsage7,DestMachineUsage8,DestMachineUsage9,");
    fprintf(trackingFile, "DestMachineUsage10,DestMachineUsage11,DestMachineUsage12,DestMachineUsage13,DestMachineUsage14,");
    fprintf(trackingFile, "DestMachineUsage15,DestMachineUsage16,DestMachineUsage17,DestMachineUsage18,DestMachineUsage19,");
    
    fprintf(trackingFile, "DestMachineCapacity0,DestMachineCapacity1,DestMachineCapacity2,DestMachineCapacity3,DestMachineCapacity4,");
    fprintf(trackingFile, "DestMachineCapacity5,DestMachineCapacity6,DestMachineCapacity7,DestMachineCapacity8,DestMachineCapacity9,");
    fprintf(trackingFile, "DestMachineCapacity10,DestMachineCapacity11,DestMachineCapacity12,DestMachineCapacity13,DestMachineCapacity14,");
    fprintf(trackingFile, "DestMachineCapacity15,DestMachineCapacity16,DestMachineCapacity17,DestMachineCapacity18,DestMachineCapacity19,");
    
    fprintf(trackingFile, "DestMachineProcessCount,SourceMachineProcessCount,");
    fprintf(trackingFile, "LoadCost,BalanceCost,SolutionCost\n");
}

void trackProcessReassignment(usint processId, usint sourceMachine, usint destMachine) {
    long long int moveCost;
    long long int improvement;
    
    if (!trackingEnabled || trackingFile == NULL) return;
    
    /* Skip tracking if it's not a real reassignment (assign to same machine) */
    if (sourceMachine == destMachine) return;
    
    moveNumber++;
    
    /* Calculate move cost and improvement */
    moveCost = getCurrentMoveCost(processId, sourceMachine, destMachine);
    improvement = 0; /* CB-LNS tracks absolute cost rather than improvement */
    
    writeProcessReassignmentData(processId, sourceMachine, destMachine, moveCost, improvement);
    
    /* Flush to ensure data is written */
    fflush(trackingFile);
}

long long int getCurrentMoveCost(usint processId, usint sourceMachine, usint destMachine) {
    /* For CB-LNS, use the move cost calculation */
    if (destMachine != OM[processId]) {
        return processMoveCost(processId) + machineMoveCost(processId);
    }
    return 0;
}

void writeProcessReassignmentData(usint processId, usint sourceMachine, usint destMachine, 
                                  long long int moveCost, long long int improvement) {
    time_t currentTime;
    int r, b;
    long long int totalLoadCost = 0;
    long long int totalBalanceCost = 0;
    
    if (trackingFile == NULL) return;
    
    currentTime = time(NULL);
    
    /* Basic reassignment data */
    fprintf(trackingFile, "%d,%d,%d,%d,%d,", 
            moveNumber, processId, sourceMachine, destMachine, OM[processId]);
    fprintf(trackingFile, "%d,%lld,", S[processId], moveCost);
    
    /* Process resource requirements (20 resources) */
    for (r = 0; r < 20; r++) {
        if (r < no_resources) {
            fprintf(trackingFile, "%d,", R[processId][r]);
        } else {
            fprintf(trackingFile, "0,");
        }
    }
    
    fprintf(trackingFile, "%lld,%ld,1,", improvement, currentTime - trackingStartTime);
    
    /* Destination machine resource usage (20 resources) */
    for (r = 0; r < 20; r++) {
        if (r < no_resources) {
            fprintf(trackingFile, "%lld,", usage[destMachine][r]);
        } else {
            fprintf(trackingFile, "0,");
        }
    }
    
    /* Destination machine resource capacities (20 resources) */
    for (r = 0; r < 20; r++) {
        if (r < no_resources) {
            fprintf(trackingFile, "%d,", machines[destMachine].capacities[r]);
        } else {
            fprintf(trackingFile, "0,");
        }
    }
    
    /* Process counts and costs */
    fprintf(trackingFile, "%d,%d,", machines[destMachine].n, machines[sourceMachine].n);
    
    /* Load cost, balance cost, and total solution cost */
    
    /* Calculate load costs for destination machine */
    for (r = 0; r < no_resources; r++) {
        totalLoadCost += loadCost(destMachine, r) * weight_lc[r];
    }
    
    /* Calculate balance costs for destination machine */
    for (b = 0; b < no_balances; b++) {
        totalBalanceCost += balanceCost(destMachine, b) * balances[b].weight_bc;
    }
    
    fprintf(trackingFile, "%lld,%lld,%llu\n", totalLoadCost, totalBalanceCost, objective_cost);
}

void enableTracking(void) {
    trackingEnabled = 1;
}

void disableTracking(void) {
    trackingEnabled = 0;
}

void updatePreviousMachineState(void) {
    int i;
    
    if (!trackingEnabled || previousMachine == NULL) return;
    
    /* Update previous machine state to current state */
    for (i = 0; i < no_processes; i++) {
        previousMachine[i] = NM[i];
    }
}

void trackCurrentReassignments(void) {
    int i;
    
    if (!trackingEnabled || previousMachine == NULL) return;
    
    /* Track all processes that were reassigned */
    for (i = 0; i < no_processes; i++) {
        if (previousMachine[i] != NM[i] && previousMachine[i] != UNASSIGNED && NM[i] != UNASSIGNED) {
            trackProcessReassignment(i, previousMachine[i], NM[i]);
        }
    }
}

void finalizeTracking(void) {
    if (trackingFile != NULL) {
        fclose(trackingFile);
        trackingFile = NULL;
    }
    
    if (trackingFilename != NULL) {
        free(trackingFilename);
        trackingFilename = NULL;
    }
    
    if (previousMachine != NULL) {
        free(previousMachine);
        previousMachine = NULL;
    }
    
    trackingEnabled = 0;
    printf("Tracking finalized. Total moves tracked: %d\n", moveNumber);
}
