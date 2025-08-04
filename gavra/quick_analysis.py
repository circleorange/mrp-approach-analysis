#!/usr/bin/env python3
"""
Quick analysis script for S41 algorithm results.
Usage: python3 quick_analysis.py <results_directory>
"""

import sys
import pandas as pd
import os

def quick_analysis(results_dir):
    """Perform quick analysis of tracking results."""
    
    print(f"Analyzing results in: {results_dir}")
    print("=" * 60)
    
    # Check for tracking files
    sol1_file = os.path.join(results_dir, "process_reassignments_sol1.csv")
    sol2_file = os.path.join(results_dir, "process_reassignments_sol2.csv")
    
    if not os.path.exists(sol1_file) or not os.path.exists(sol2_file):
        print("Error: Tracking files not found!")
        return
    
    # Load data (just first and last rows for efficiency)
    print("Loading tracking data...")
    
    # Get basic info without loading entire files
    sol1_lines = sum(1 for line in open(sol1_file)) - 1  # Subtract header
    sol2_lines = sum(1 for line in open(sol2_file)) - 1
    
    # Load first and last few rows
    sol1_first = pd.read_csv(sol1_file, nrows=5)
    sol1_last = pd.read_csv(sol1_file, skiprows=range(1, sol1_lines-4))
    
    sol2_first = pd.read_csv(sol2_file, nrows=5)
    sol2_last = pd.read_csv(sol2_file, skiprows=range(1, sol2_lines-4))
    
    print(f"\nSolution 1:")
    print(f"  Total moves: {sol1_lines:,}")
    print(f"  Initial cost: {sol1_first['SolutionCost'].iloc[0]:,}")
    print(f"  Final cost: {sol1_last['SolutionCost'].iloc[-1]:,}")
    print(f"  Improvement: {sol1_first['SolutionCost'].iloc[0] - sol1_last['SolutionCost'].iloc[-1]:,}")
    
    print(f"\nSolution 2:")
    print(f"  Total moves: {sol2_lines:,}")
    print(f"  Initial cost: {sol2_first['SolutionCost'].iloc[0]:,}")
    print(f"  Final cost: {sol2_last['SolutionCost'].iloc[-1]:,}")
    print(f"  Improvement: {sol2_first['SolutionCost'].iloc[0] - sol2_last['SolutionCost'].iloc[-1]:,}")
    
    # Determine better solution
    sol1_final = sol1_last['SolutionCost'].iloc[-1]
    sol2_final = sol2_last['SolutionCost'].iloc[-1]
    
    print(f"\nBest solution: {'Solution 1' if sol1_final < sol2_final else 'Solution 2'}")
    print(f"Best cost: {min(sol1_final, sol2_final):,}")
    
    print(f"\nTotal algorithm activity: {sol1_lines + sol2_lines:,} moves")
    
    # Check if solution file exists
    solution_file = None
    for f in os.listdir(results_dir):
        if f.startswith("solution_") and f.endswith(".txt"):
            solution_file = f
            break
    
    if solution_file:
        print(f"Final solution saved to: {solution_file}")
    
    print("\n" + "=" * 60)
    print("For detailed analysis, use the Jupyter notebook:")
    print(f"  cd {results_dir}")
    print("  jupyter notebook ../analytics/analysis.ipynb")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 quick_analysis.py <results_directory>")
        sys.exit(1)
    
    results_dir = sys.argv[1]
    if not os.path.exists(results_dir):
        print(f"Error: Directory {results_dir} does not exist!")
        sys.exit(1)
    
    quick_analysis(results_dir)
