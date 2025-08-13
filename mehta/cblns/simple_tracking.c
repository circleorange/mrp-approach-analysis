/**************************************************************************************************
	SIMPLE TRACKING FOR MEHTA CB-LNS - Minimal implementation
	
	This provides basic tracking without conflicts with the existing global variable structure.
	Uses static local variables to avoid multiple definition issues.
 **************************************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static FILE *tracking_file = NULL;
static char tracking_filename[256];
static int tracking_move_number = 0;
static time_t tracking_start_time;
static int tracking_initialized = 0;
static unsigned int current_solution_id = 0;

/* Simple tracking functions that don't depend on global variables */
void simple_init_tracking(const char* filename) {
    if (tracking_initialized) return;
    
    strncpy(tracking_filename, filename, sizeof(tracking_filename) - 1);
    tracking_filename[sizeof(tracking_filename) - 1] = '\0';
    
    tracking_file = fopen(tracking_filename, "w");
    if (!tracking_file) {
        printf("Warning: Could not open tracking file %s\n", tracking_filename);
        return;
    }
    
    tracking_start_time = time(NULL);
    tracking_move_number = 0;
    tracking_initialized = 1;
    
    /* Write CSV header */
    fprintf(tracking_file, "moveNumber,processId,sourceMachine,destMachine,moveCost,improvement,timestamp,solutionId,solutionCost\n");
    fflush(tracking_file);
    
    printf("Simple tracking initialized: %s\n", tracking_filename);
}

void simple_track_move(unsigned short processId, unsigned short sourceMachine, 
                      unsigned short destMachine, long long moveCost, 
                      unsigned int solutionId, long long solutionCost) {
    double timestamp;
    long long improvement;
    
    if (!tracking_initialized || !tracking_file) return;
    
    tracking_move_number++;
    improvement = -moveCost; /* Assume cost is always a penalty, so improvement is negative cost */
    timestamp = difftime(time(NULL), tracking_start_time);
    
    fprintf(tracking_file, "%d,%u,%u,%u,%lld,%lld,%.2f,%u,%lld\n",
            tracking_move_number, processId, sourceMachine, destMachine, 
            moveCost, improvement, timestamp, solutionId, solutionCost);
    fflush(tracking_file);
}

unsigned int simple_get_next_solution_id(void) {
    return ++current_solution_id;
}

void simple_finalize_tracking(void) {
    if (!tracking_initialized) return;
    
    if (tracking_file) {
        fclose(tracking_file);
        tracking_file = NULL;
    }
    
    tracking_initialized = 0;
    printf("Simple tracking finalized: %s\n", tracking_filename);
}

/* Test function */
int test_simple_tracking(void) {
    printf("Testing simple tracking...\n");
    
    simple_init_tracking("simple_tracking_test.csv");
    
    /* Test some moves */
    simple_track_move(0, 0, 1, 150, 1, 10000);
    simple_track_move(1, 2, 3, 200, 2, 9800);
    simple_track_move(2, 1, 0, 75, 3, 9725);
    
    simple_finalize_tracking();
    
    printf("Simple tracking test completed.\n");
    return 0;
}
