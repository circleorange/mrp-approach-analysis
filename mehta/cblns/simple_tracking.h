/**************************************************************************************************
	SIMPLE TRACKING HEADER - Minimal tracking interface for MEHTA CB-LNS
 **************************************************************************************************/

#ifndef _SIMPLE_TRACKING_H
#define _SIMPLE_TRACKING_H 1

/* Simple tracking functions that don't conflict with global variables */
void simple_init_tracking(const char* filename);
void simple_track_move(unsigned short processId, unsigned short sourceMachine, 
                      unsigned short destMachine, long long moveCost, 
                      unsigned int solutionId, long long solutionCost);
unsigned int simple_get_next_solution_id(void);
void simple_finalize_tracking(void);

/* Test function */
int test_simple_tracking(void);

#endif /* _SIMPLE_TRACKING_H */
