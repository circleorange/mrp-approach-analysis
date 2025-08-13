/**************************************************************************************************
	Copyright 2011 Deepak Mehta, Barry O'Sullivan, Helmut Simonis, University College Cork, Ireland

	This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU  General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU  General Public License for more details.

    You should have received a copy of the GNU  General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 **************************************************************************************************/



#ifndef _DEFINITIONS_H
#define _DEFINITIONS_H 1


#include<time.h>
#include<stdio.h>
#define CALLOC( nmemb, size ) calloc( nmemb, size )
#define TRUE 1
#define FALSE 0
#define USED  2
#define CANNOTBEUSED 1
#define AVAILABLE 0
#define UNASSIGNED 60000
#define NONE 60000
/*#define assertion 1*/

typedef unsigned short int usint ;
typedef char boolean ;
typedef unsigned int uint;

extern usint no_resources ;
extern usint no_machines;
extern usint no_services;
extern usint no_processes ;
extern usint no_balances ;
extern usint no_locations;
extern usint no_neighborhoods;

extern unsigned int *transient ;
extern unsigned int *weight_lc;

typedef struct machine_struct {
  usint neighborhood;
  usint location;
  usint *processes;
  usint size;
  usint n;
  unsigned int *capacities;
  unsigned int *scapacities;
  unsigned int *mmc;
} MACHINE, *MACHINE_PTR;

extern MACHINE *machines ;
extern char **msrop;
extern unsigned int **R; 
extern usint maxno_processes_moved_in_service ;

typedef struct service_struct{
  /* the following are not changing during search */
  usint spreadMin ;
  usint no_of_processes;
  usint no_dependson;     /* number of dependencies of the service (it is not changing during search) */   
  usint *dependson ;        /* array of services on which the current service is depending on (this is not changing during search */
	
  /* the following are required to be maintained during search only when the service is involved in some dependency */
  usint *unassigned_process;
  usint no_of_unassigned_processes;

  usint no_of_moved_processes;

  char *used_machines ;  /* set TRUE to those machines are in use */
  usint no_of_used_machines ;
  usint no_of_available_machines ;

  usint *used_locations;
  usint no_of_used_locations; 

  usint *neighborhood;
  usint no_of_neighborhoods; /* last index of the  current neighborhoods (changing)*/    
  usint *used_neighborhoods;   /* table for checking which neighborhoods are in use (changing) */
  usint no_of_mandatory_neighborhoods;
  usint *mandatory_neighborhoods;
} SERVICE, *SERVICE_PTR;

extern SERVICE *services;

extern usint *S ;



typedef struct balance_obj_struct {
   unsigned int i;
   unsigned int j;
   unsigned int target;
   unsigned int weight_bc;
} BALANCE, *BALANCE_PTR ;

extern BALANCE *balances;

extern unsigned int weight_pmc;
extern unsigned int weight_smc;
extern unsigned int weight_mmc;

extern long long int **usage;
extern long long int **tusage;
extern unsigned int *pmc ;

extern unsigned long long int objective_cost ;
extern long long int *machine_cost;

extern unsigned short int *OM, *NM, *BM;
extern unsigned short int *previous_BM;  /* Previous best solution for tracking accepted changes */
extern unsigned short int **values;
extern unsigned short int *dsize;

extern unsigned short int *active_services ;
extern unsigned short int no_of_active_services;

extern long long int **pmcost, **movecost;
extern unsigned long long *process_requirement_cost ;
extern unsigned long long int *demand;
extern unsigned long long int *supply;

extern long long *costOfProcess ;
extern usint *bestM;

extern unsigned  int time_limit, print_time ;
extern time_t start_time;
extern int seed;
/*unsigned int *process_failures ;*/
/* no of machines availables for a processes that satisfy resource requirements */
extern usint *no_available_machines;

/* solution file */ 
extern char *solutionfilename ;
extern char *default_sol_filename ;
/* log file */
extern FILE *logfile;
extern char *logfilename;
extern char *modelfilename;
extern char *iassignmentfilename;
extern char printinfile;
extern char printonscreen;


/* function pointers */

extern double (*machine_heuristic_weight)( usint const p, usint const w );
extern double (*input_machine_heuristic_weight)( usint const p, usint const w );
extern double (*service_heuristic_weight)( usint const w );
extern double (*process_heuristic_weight)( usint const w );
extern usint (*select_and_remove_process)(void);
extern void (*restore_process)(usint const p);

#endif /* definitions.h */
