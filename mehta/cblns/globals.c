/**************************************************************************************************
	GLOBAL VARIABLE DEFINITIONS FOR MEHTA CB-LNS
	
	This file contains the actual definitions of all global variables that were previously
	defined in header files. Each variable is defined exactly once here to avoid multiple
	definition errors during linking.
 **************************************************************************************************/

#include "definitions.h"
#include "search.h"
#include "selection.h"
#include "utils.h"
#include "machine.h"
#include "cost.h"

/* From definitions.h */
usint no_resources ;
usint no_machines;
usint no_services;
usint no_processes ;
usint no_balances ;
usint no_locations;
usint no_neighborhoods;

unsigned int *transient ;
unsigned int *weight_lc;

MACHINE *machines ;
char **msrop;
unsigned int **R; 
usint maxno_processes_moved_in_service ;

SERVICE *services;
usint *S ;

BALANCE *balances;

unsigned int weight_pmc;
unsigned int weight_smc;
unsigned int weight_mmc;

long long int **usage;
long long int **tusage;
unsigned int *pmc ;

unsigned long long int objective_cost ;
long long int *machine_cost;

unsigned short int *OM, *NM, *BM;
unsigned short int *previous_BM;  /* Previous best solution for tracking accepted changes */
unsigned short int **values;
unsigned short int *dsize;

unsigned short int *active_services ;
unsigned short int no_of_active_services;

long long int **pmcost, **movecost;
unsigned long long *process_requirement_cost ;
unsigned long long int *demand;
unsigned long long int *supply;

long long *costOfProcess ;
usint *bestM;

unsigned  int time_limit, print_time ;
time_t start_time;
int seed;
usint *no_available_machines;

char *solutionfilename ;
char *default_sol_filename ;
FILE *logfile;
char *logfilename;
char *modelfilename;
char *iassignmentfilename;
char printinfile;
char printonscreen;

double (*machine_heuristic_weight)( usint const p, usint const w );
double (*input_machine_heuristic_weight)( usint const p, usint const w );
double (*service_heuristic_weight)( usint const w );
double (*process_heuristic_weight)( usint const w );
usint (*select_and_remove_process)(void);
void (*restore_process)(usint const p);

/* From search.h */
int no_of_unassigned_processes,  no_of_rem_unassigned_processes ;
boolean stop_search, solution_found;
int remove_no_process;
boolean verification;

usint *unassigned_processes;
boolean *max_moved_store;
long long int *pmcost_up ;
usint *fp_up;
usint  *machineIndices ;
usint *pind;
unsigned long long int threshold, input_threshold, thresholdm;
unsigned int no_of_services_selected ;
unsigned long long int best_objective_cost;

unsigned long long int total_failures;
unsigned long long int no_of_failures ;

unsigned long long int iterations, siterations ;
int current_service_index ;
usint current_process;

void (*lns_type_selection)(int);
void (*lns)(void);
unsigned short int  *service_machines_stack, *pid_ds;
unsigned int service_machines_counter, service_machines_limit  ;

/* From selection.h */
char mh_id;

/* From utils.h */
usint current_resource ;

/* From machine.h */
char PROCESS_FAILED;

/* From cost.h */
double futureCost ;
