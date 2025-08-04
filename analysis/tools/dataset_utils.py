import numpy as np

def get_process_moves(process_id, move_ids, process_ids, src_machines, dest_machines, unique=False, print_results=False):
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

def get_machine_resource_usage(machine_id, src_machines, dest_machines, src_machine_usages, dest_machine_usages, show_results=False):
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
    if show_results:
        for i in range(min(len(machine_usages), 10)):
            print(f"Machine: {machine_id}, Usage: {machine_usages[i]}")

    return machine_usages
