/**************************************************************************************************
	TRACKING INFRASTRUCTURE FOR MACHINE REASSIGNMENT PROBLEM
	
	This file provides tracking capabilities for process reassignments during optimization.
	Compatible with JASK and GAVRA tracking implementations for cross-algorithm analysis.
	
	Usage:
	1. Call initTracking() before optimization begins
	2. Call trackProcessReassignment() for each reassignment during search  
	3. Call finalizeTracking() after optimization completes
 **************************************************************************************************/

#ifndef _TRACKING_H
#define _TRACKING_H 1

#include <time.h>
#include <stdio.h>

/* usint type will be available from definitions.h via other includes */

/* Tracking control variables - declared as extern to avoid multiple definitions */
extern int trackingEnabled;
extern int moveNumber;
extern FILE *trackingFile;
extern char *trackingFilename;
extern time_t trackingStartTime;
extern usint *previousMachine; /* Track previous machine assignment for each process */

/* Initialize tracking system */
void initTracking(const char* filename);

/* Track a single process reassignment */
void trackProcessReassignment(usint processId, usint sourceMachine, usint destMachine);

/* Finalize tracking and close file */
void finalizeTracking(void);

/* Enable/disable tracking during optimization phases */
void enableTracking(void);
void disableTracking(void);

/* Update previous machine state and track reassignments */
void updatePreviousMachineState(void);
void trackCurrentReassignments(void);

/* Utility functions for tracking data */
long long int getCurrentMoveCost(usint processId, usint sourceMachine, usint destMachine);
void writeTrackingHeader(void);
void writeProcessReassignmentData(usint processId, usint sourceMachine, usint destMachine, 
                                  long long int moveCost, long long int improvement);

#endif /* _TRACKING_H */
