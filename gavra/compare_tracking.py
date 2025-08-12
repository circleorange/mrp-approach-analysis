import pandas as pd

# Load Java tracking data
java_df = pd.read_csv('/home/pbiel/repos/mrp/jask/process_reassignments.csv', nrows=50)
print("Java implementation - MoveNum vs SolutionId:")
print(java_df[['MoveNum', 'SolutionId']].head(20))

print("\nUnique solution IDs in first 50 moves:")
print(f"Total moves: {len(java_df)}")
print(f"Unique solution IDs: {java_df['SolutionId'].nunique()}")
print(f"Solution ID values: {sorted(java_df['SolutionId'].unique())}")

# Load C++ tracking data  
cpp_df = pd.read_csv('/home/pbiel/repos/mrp/gavra/results_a1_2_20250810_144506/process_reassignments_sol1.csv', nrows=50)
print("\n" + "="*50)
print("C++ implementation - MoveNum vs SolutionId:")
print(cpp_df[['MoveNum', 'SolutionId']].head(20))

print("\nUnique solution IDs in first 50 moves:")
print(f"Total moves: {len(cpp_df)}")
print(f"Unique solution IDs: {cpp_df['SolutionId'].nunique()}")
print(f"Solution ID values: {sorted(cpp_df['SolutionId'].unique())}")
