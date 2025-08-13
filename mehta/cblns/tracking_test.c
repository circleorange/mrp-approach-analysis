/**************************************************************************************************
	TRACKING TEST PROGRAM - Standalone test for tracking infrastructure
	Tests tracking functionality independently of the main MEHTA executable
 **************************************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* Minimal definitions needed for tracking test */
typedef unsigned short int usint;

/* Tracking variables - defined here for standalone test */
int trackingEnabled = 0;
int moveNumber = 0;
FILE *trackingFile = NULL;
char *trackingFilename = NULL;
time_t trackingStartTime;
usint *previousMachine = NULL;

/* Mock global data for testing */
usint no_processes = 10;
usint no_machines = 5;
usint no_resources = 3;

/* Mock function declarations */
void initTracking(const char* filename);
void trackProcessReassignment(usint processId, usint sourceMachine, usint destMachine);
void writeTrackingHeader(void);
void finalizeTracking(void);

/* Implementation of tracking functions */
void initTracking(const char* filename) {
    int i;
    
    trackingFilename = (char*)malloc(strlen(filename) + 1);
    strcpy(trackingFilename, filename);
    
    trackingFile = fopen(trackingFilename, "w");
    if (!trackingFile) {
        printf("Error: Could not open tracking file %s\n", trackingFilename);
        return;
    }
    
    /* Initialize previous machine state */
    previousMachine = (usint*)calloc(no_processes, sizeof(usint));
    for (i = 0; i < no_processes; i++) {
        previousMachine[i] = i % no_machines; /* Mock initial assignment */
    }
    
    trackingStartTime = time(NULL);
    moveNumber = 0;
    trackingEnabled = 1;
    
    writeTrackingHeader();
    printf("Tracking initialized: %s\n", trackingFilename);
}

void writeTrackingHeader(void) {
    if (!trackingFile) return;
    
    fprintf(trackingFile, "moveNumber,processId,sourceMachine,destMachine,moveCost,improvement,timestamp\n");
    fflush(trackingFile);
}

void trackProcessReassignment(usint processId, usint sourceMachine, usint destMachine) {
    long long int moveCost, improvement;
    double timestamp;
    
    if (!trackingEnabled || !trackingFile) return;
    
    /* Mock cost calculation */
    moveCost = abs((int)destMachine - (int)sourceMachine) * 100;
    improvement = moveCost > 0 ? -moveCost : moveCost;
    timestamp = difftime(time(NULL), trackingStartTime);
    
    moveNumber++;
    
    fprintf(trackingFile, "%d,%u,%u,%u,%lld,%lld,%.2f\n",
            moveNumber, processId, sourceMachine, destMachine, 
            moveCost, improvement, timestamp);
    fflush(trackingFile);
    
    /* Update previous machine state */
    previousMachine[processId] = destMachine;
    
    printf("Tracked move %d: Process %u from machine %u to %u (cost: %lld)\n",
           moveNumber, processId, sourceMachine, destMachine, moveCost);
}

void finalizeTracking(void) {
    if (trackingFile) {
        fclose(trackingFile);
        trackingFile = NULL;
    }
    
    if (trackingFilename) {
        free(trackingFilename);
        trackingFilename = NULL;
    }
    
    if (previousMachine) {
        free(previousMachine);
        previousMachine = NULL;
    }
    
    trackingEnabled = 0;
    printf("Tracking finalized\n");
}

/* Test program main function */
int main(void) {
    printf("MEHTA Tracking Infrastructure Test\n");
    printf("==================================\n");
    
    /* Test tracking functionality */
    initTracking("test_tracking.csv");
    
    /* Simulate some process reassignments */
    trackProcessReassignment(0, 0, 1);
    trackProcessReassignment(1, 1, 3);
    trackProcessReassignment(2, 2, 0);
    trackProcessReassignment(3, 3, 2);
    trackProcessReassignment(4, 4, 1);
    
    finalizeTracking();
    
    printf("\nTest completed. Check test_tracking.csv for output.\n");
    return 0;
}
