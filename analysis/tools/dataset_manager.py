import numpy as np
import pandas as pd
import ast
import inspect

DEBUG = True

def log(message):
    # Get the name of the function that called
    if not DEBUG: return
    caller = inspect.currentframe().f_back.f_code.co_name
    print(f"[{caller}] - {message}")

class SolutionStatesDataset:
    # SolutionId,Cost,Improvement,Timestamp,SolverMethod,NumReassignments,LoadCost,BalanceCost,MachineMoveCost,ProcessMoveCost,ServiceMoveCost,NumConstraintsUnsatisfied,IsFeasible
    # 1,1061649570,0.0000,1753739591597,"HillClimber-Initial",0,1061649570,0,0,0,0,0,true
    # 2,1035867931,2.4285,1753739591608,"HillClimber-Greedy",1,1035867720,0,200,1,10,0,true
    # 3,1020978102,3.8310,1753739591610,"HillClimber-Greedy",4,1020977790,0,300,2,10,0,true

    def __init__(self, path):
        pass

class ReassignmentsDataset:
    # timestamp       : pd.Series  # Timestamps in pandas datetime format

    # >>>>> Reassignment (Move) Data >>>>>
    move_id    : np.ndarray  # Reassignment (Move) ID
    solution_id: np.ndarray  # Solution ID
    service_id : np.ndarray  # Service ID

    # >>>>> Process Data >>>>>
    ps_id           : np.ndarray  # Process ID
    ps_size         : np.ndarray  # Total Process Requirements (sum per process)

    # >>>>> Machine, Solution, and Service Data >>>>>
    src_machine_id             : np.ndarray  # Source Machine ID
    src_machine_usage          : np.ndarray  # Source Machine Resource Usage
    src_machine_capacity       : np.ndarray  # Source Machine Capacities
    src_machine_transient_usage: np.ndarray  # Source Machine Transient Usage
    src_machine_ps_count       : int          # Source Machine Process Count

    dest_machine_id             : np.ndarray  # Destination Machine ID
    dest_machine_usage          : np.ndarray  # Destination Machine Resource Usage
    dest_machine_capacity       : np.ndarray  # Destination Machine Capacities
    dest_machine_transient_usage: np.ndarray  # Destination Machine Transient Usage
    dest_machine_ps_count       : int          # Destination Machine Process Count

    # >>>>> Cost Data >>>>>
    solution_cost_improvement: np.ndarray  # Improvement from Process Reassignment
    move_cost                : np.ndarray  # Move Cost
    load_cost                : np.ndarray  # Load Cost
    balance_cost             : np.ndarray  # Balance Cost
    solution_cost            : np.ndarray  # Solution Cost

    def __init__(self, dataset_fraction: float = 1.0):
        raw_reassignments_dataset_path = "/home/pbiel/repos/jask/analytics/a12_new/process_reassignments.csv"
        df = pd.read_csv(raw_reassignments_dataset_path)
        print(f"Loading {len(df)} entries frm dataset: {raw_reassignments_dataset_path}.")

        # Select only portion of the dataset
        N = int(len(df) * dataset_fraction)
        df = df[:N]
        # df = df.sample(frac=0.2, random_state=42) # Sample 20% of the dataset
        
        print(f"Sampled dataset to {len(df)} entries.")

        # >>>>> Data initialization >>>>>

        # self.timestamp = pd.to_datetime(self.df['Timestamp'], unit='ms', format='%Y-%m-%d %H:%M:%S.%f')
        self.move_id               = df['MoveNum'].values
        self.ps_id                 = df['ProcessID'].values
        self.solution_id           = df['SolutionId'].values
        self.service_id            = df['Service'].values
        self.src_machine_id        = df['SourceMachine'].values
        self.src_machine_ps_count  = df['SourceMachineProcessCount'].values
        self.dest_machine_id       = df['DestMachine'].values
        self.dest_machine_ps_count = df['DestMachineProcessCount'].values

        self.move_cost                 = df['MoveCost'].values
        self.load_cost                 = df['LoadCost'].values
        self.balance_cost              = df['BalanceCost'].values
        self.solution_cost             = df['SolutionCost'].values
        self.solution_cost_improvement = df['Improvement'].values

        # >>>>> Process and Machine Resources, Usages, and Capacities >>>>>

        self.ps_size                      = self.__sum_matrix(df['ProcessResourceRequirements'], axis=1)
        self.src_machine_usage            = self.__sum_matrix(df['SourceMachineResourceUsage'], axis=1)
        self.src_machine_capacity         = self.__sum_matrix(df['SourceMachineCapacities'], axis=1)
        self.src_machine_transient_usage  = self.__sum_matrix(df['SourceMachineTransientUsage'], axis=1)
        self.dest_machine_usage           = self.__sum_matrix(df['DestMachineResourceUsage'], axis=1)
        self.dest_machine_capacity        = self.__sum_matrix(df['DestMachineCapacities'], axis=1)
        self.dest_machine_transient_usage = self.__sum_matrix(df['DestMachineTransientUsage'], axis=1)

        print("Completed loading dataset.")

    def transition_statistics(self):
        solution_states = self.solution_state_change_points()
        transitions_reassignments_counts = self.transitions_reassignments_count()

        transition_sizes = np.zeros(len(solution_states) - 1, dtype=int)
        transition_means = np.zeros(len(solution_states) - 1, dtype=float)
        transition_min = np.zeros(len(solution_states) - 1, dtype=int)
        transition_max = np.zeros(len(solution_states) - 1, dtype=int)
        transition_diff = np.zeros(len(solution_states) - 1, dtype=float)

        for i in range(len(solution_states) - 1):
            transition_start = solution_states[i]
            transition_end = solution_states[i + 1]
            transition_ps_size = self.ps_size[transition_start:transition_end]

            transition_moves_count = transitions_reassignments_counts[i]
            transition_sizes[i] = np.sum(transition_ps_size)
            transition_means[i] = transition_sizes[i] / transition_moves_count
            transition_min[i] = np.min(transition_ps_size)
            transition_max[i] = np.max(transition_ps_size)
            transition_diff[i] = transition_max[i] - transition_min[i]

            if DEBUG and (i < 5 or i > len(solution_states) - 5):
                log(f"transition {i}: moves: {len(transition_ps_size)}, total_size={transition_sizes[i]}, mean={transition_means[i]}, min={transition_min[i]}, max={transition_max[i]}, diff={transition_diff[i]}")

        return transition_sizes, transition_means, transition_min, transition_max, transition_diff

    def transitions_reassignments_count(self) -> np.ndarray:
        solution_states = self.solution_state_change_points()
        transition_moves = np.diff(solution_states)

        if DEBUG: log(f"shape: {np.shape(transition_moves)}\n{transition_moves[:5]} ... {transition_moves[-5:]}")

        return transition_moves

    def solution_cost_improvement_deltas(self) -> list[float]:
        change_idx = self.solution_state_change_points()  # returns; [1, 2, 5, 14, ...]
        transition_states_idx = change_idx[:-1]
        deltas = np.diff(self.solution_cost_improvement[transition_states_idx], prepend=0)
        deltas = np.round(deltas, 5)

        if DEBUG: log(f"shape: {np.shape(deltas)}\nsamples: {deltas[:5]} ... {deltas[-5:]}")
        
        return deltas

    def solution_state_change_points(self) -> np.ndarray:
        new_solution_idx = np.flatnonzero(np.diff(self.solution_id) != 0) + 1
        # Prepend transition from initial assignment to solution 1
        new_solution_idx = np.r_[0, new_solution_idx]
        if new_solution_idx[-1] != len(self.move_id): 
            # Treat the very last move as the final solution state change
            # This is the case when the last solution has moves but is not counted in np.diff
            new_solution_idx = np.r_[new_solution_idx, len(self.move_id)]

        if DEBUG: log(f"shape: {np.shape(new_solution_idx)}\n{new_solution_idx[:5]} ... {new_solution_idx[-5:]}")

        return new_solution_idx

    def get_process_moves(self, process_id, move_ids, process_ids, src_machines, dest_machines, unique=False, print_results=False):
        """
        Get all moves for a given process ID.
        If unique is True, return unique source and destination machines.
        """
        mask = (process_ids == process_id)

        move_id_matches = move_ids[mask]
        src_machine_matches = src_machines[mask]
        dest_machine_matches = dest_machines[mask]

        if unique:
            # Preserve first-order seen while removing duplicates
            _, src_machine_idx = np.unique(src_machine_matches, return_index=True)
            _, dest_machine_idx = np.unique(dest_machine_matches, return_index=True)
            
            move_id_matches = move_id_matches[np.sort(np.concatenate((src_machine_idx, dest_machine_idx)))]
            src_machine_matches = src_machine_matches[np.sort(src_machine_idx)]
            dest_machine_matches = dest_machine_matches[np.sort(dest_machine_idx)]
        
        print(f"Returning {len(move_id_matches)} results for process {process_id}.")

        if print_results:
            for i in range(len(move_id_matches)):
                process_id, move_id, src_machine, dest_machine = process_id, move_id_matches[i], src_machine_matches[i], dest_machine_matches[i]
                print(f"Process: {process_id}, Move ID: {move_id}, Source Machine: {src_machine}, Destination Machine: {dest_machine}")

        return move_id_matches, src_machine_matches, dest_machine_matches

    def get_machine_resource_usage(self, machine_id, src_machines, dest_machines, src_machine_usages, dest_machine_usages, print_results=False):
            """
            Returns list where each element is the usage snapshot of the machine at the time of the move.
            """
            matches_as_src_machine  = np.where(src_machines == machine_id)[0]
            matches_as_dest_machine = np.where(dest_machines == machine_id)[0]

            machine_usages = []

            for idx in matches_as_src_machine:
                machine_usages.append(src_machine_usages[idx])

            for idx in matches_as_dest_machine:
                machine_usages.append(dest_machine_usages[idx])

            print(f"Returning {len(machine_usages)} results for machine {machine_id}.")
            if print_results:
                for i in range(min(len(machine_usages), 10)):
                    print(f"Machine: {machine_id}, Usage: {machine_usages[i]}")

            return machine_usages

    def __parse_raw_list_of_values(self, ls) -> np.ndarray:
        try:              return np.array(ast.literal_eval(ls), dtype=int)
        except Exception: return np.zeros(len(ls), dtype=int)
    
    def __sum_matrix(self, df, axis=1) -> np.ndarray:
        df_parsed = df.apply(self.__parse_raw_list_of_values)
        np_mtx = np.stack(df_parsed.values)
        np_arr = np.sum(np_mtx, axis=axis) # Sum each row, e.g. total requirements per process
        return np_arr

    def metadata(self):
        print(">>> Basic Metadata >>>")
        print(f"Total Moves: {len(self.move_id)}")
        print(f"Total Processes: {len(np.unique(self.ps_id))}")
        print(f"Total Machines: {len(np.unique(self.src_machine_id))}")
        print(f"Total Solutions: {len(np.unique(self.solution_id))}")
        print(f"Total Services: {len(np.unique(self.service_id))}")

        print(">>> Process Sizes >>>")
        print(f"Process Sizes Shape: {self.ps_size.shape}")
        print(f"Process Sizes: {self.ps_size[:10]}...")  # Print first 10 process sizes
        print(f"Process size - Max: {np.max(self.ps_size)}, Min: {np.min(self.ps_size)}")

        print(">>> Move Cost Distribution Stats >>>")
        print(f"Move Costs Shape: {self.move_cost.shape}")
        print(f"Move Cost Improvement Shape: {self.solution_cost_improvement.shape}")

    def uniques(self, arr: np.ndarray) -> np.ndarray:
            return np.unique(arr)

    def n_largest(self, arr, n=5, print_results=False):
            """
            Return n largest values and their indices from a 1D numpy array.
            Output: (indices, values), both sorted by descending value.

            Example:
            >>> idx, vals = n_largest(x, 3)
            >>> print(vals, idx) # Output: Indices: [3 5 1]   Values: [9 8 7]
            """
            if n > arr.size: n = arr.size
            idx_unsorted = np.argpartition(-arr, n-1)[:n] # Get indices of the n largest elements (not guaranteed sorted)
            idx_sorted = idx_unsorted[np.argsort(-arr[idx_unsorted])] # Sort those indices by value (descending)
            vals_sorted = arr[idx_sorted] # Get values
            if print_results:
                for idx, val in zip(idx_sorted, vals_sorted):
                    print(f"Move ID: {self.move_id[idx]}, Process ID: {self.ps_id[idx]}, Size: {val}")

            return idx_sorted, vals_sorted

    def n_smallest(self, arr, n=5, print_results=False):
            """
            Return n smallest values and their indices from a 1D numpy array.
            Output: (indices, values), both sorted by ascending value.

            Example:
            >>> idx, vals = n_smallest(x, 3)
            >>> print(vals, idx) # Output: Indices: [2 4 0]   Values: [1 2 3]
            """
            if n <= 0: return np.array([], dtype=int), np.array([], dtype=arr.dtype)
            if n > arr.size: n = arr.size
            idx_unsorted = np.argpartition(arr, n-1)[:n] # Get indices of the n smallest elements (not guaranteed sorted)
            idx_sorted = idx_unsorted[np.argsort(arr[idx_unsorted])] # Sort those indices by value (ascending)
            vals_sorted = arr[idx_sorted] # Get values

            if print_results:
                for idx, val in zip(idx_sorted, vals_sorted):
                    print(f"Move ID: {self.move_id[idx]}, Process ID: {self.ps_id[idx]}, Size: {val}")

            return idx_sorted, vals_sorted

    def get_col(matrix, col_idx):
            return matrix[:, col_idx]

    def get_col_range(matrix, col_idx_start, col_idx_end):
            return matrix[:, col_idx_start:col_idx_end]

    def get_row(matrix, row_idx):
            return matrix[row_idx, :]

    def get_row_range(matrix, row_idx_start, row_idx_end):
            return matrix[row_idx_start:row_idx_end, :]

