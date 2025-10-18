#!/usr/bin/env python3
"""
Moore Curve Visualizer
Creates ASCII art visualizations of Moore curve paths for different grid sizes.
"""

import sys
import os
import math

# Add the current directory to the path to import from harvest_single
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from harvest_single import generate_moore_curve_lsystem, moore_curve_to_path, generate_moore_curve_path


def create_ascii_grid(size, path):
    """Create an ASCII representation of the Moore curve path on a grid"""
    # Create a 2D grid with extra space for connections
    grid_width = size * 2 - 1
    grid_height = size * 2 - 1
    grid = [[' ' for _ in range(grid_width)] for _ in range(grid_height)]
    
    # Place numbers at each position
    for i, (x, y) in enumerate(path):
        grid_y = (size - 1 - y) * 2  # Flip Y axis for display
        grid_x = x * 2
        if 0 <= grid_y < grid_height and 0 <= grid_x < grid_width:
            # Use modulo to handle large numbers
            num = i % 100
            if num < 10:
                grid[grid_y][grid_x] = str(num)
            else:
                grid[grid_y][grid_x] = str(num // 10)
    
    # Draw connections between consecutive points
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        
        # Convert to grid coordinates
        gx1, gy1 = x1 * 2, (size - 1 - y1) * 2
        gx2, gy2 = x2 * 2, (size - 1 - y2) * 2
        
        # Calculate connection symbol
        dx = gx2 - gx1
        dy = gy2 - gy1
        
        if dx == 2 and dy == 0:  # Right
            symbol = '─'
        elif dx == -2 and dy == 0:  # Left
            symbol = '─'
        elif dx == 0 and dy == 2:  # Down
            symbol = '│'
        elif dx == 0 and dy == -2:  # Up
            symbol = '│'
        elif dx == 2 and dy == 2:  # Down-Right
            symbol = '╲'
        elif dx == -2 and dy == 2:  # Down-Left
            symbol = '╱'
        elif dx == 2 and dy == -2:  # Up-Right
            symbol = '╱'
        elif dx == -2 and dy == -2:  # Up-Left
            symbol = '╲'
        else:
            symbol = '·'
        
        # Place connection symbol
        conn_x = (gx1 + gx2) // 2
        conn_y = (gy1 + gy2) // 2
        if 0 <= conn_y < grid_height and 0 <= conn_x < grid_width:
            grid[conn_y][conn_x] = symbol
    
    return grid


def print_moore_curve(size):
    """Print a Moore curve for the given size"""
    print(f"\n{'='*60}")
    print(f"Moore Curve for {size}x{size} Grid")
    print(f"{'='*60}")
    
    # Generate the path
    path = generate_moore_curve_path(size)
    
    print(f"Path length: {len(path)}")
    print(f"Unique positions: {len(set(path))}")
    print(f"Grid coverage: {len(set(path))}/{size*size} ({100*len(set(path))//(size*size)}%)")
    
    # Create and print ASCII grid
    grid = create_ascii_grid(size, path)
    
    print(f"\nASCII Visualization:")
    print("┌" + "─" * (len(grid[0]) * 2 - 1) + "┐")
    for row in grid:
        print("│" + "".join(row) + "│")
    print("└" + "─" * (len(grid[0]) * 2 - 1) + "┘")
    
    # Print path coordinates
    print(f"\nPath coordinates:")
    for i, (x, y) in enumerate(path[:20]):  # Show first 20 positions
        print(f"  {i:2d}: ({x},{y})")
    if len(path) > 20:
        print(f"  ... and {len(path) - 20} more positions")


def print_moore_curve_simple(size):
    """Print a simple Moore curve visualization"""
    print(f"\nMoore Curve {size}x{size}:")
    
    # Generate the path
    path = generate_moore_curve_path(size)
    
    # Create a simple grid showing the order
    grid = [['.' for _ in range(size)] for _ in range(size)]
    
    for i, (x, y) in enumerate(path):
        if 0 <= x < size and 0 <= y < size:
            # Use modulo to handle large numbers
            num = i % 100
            if num < 10:
                grid[size - 1 - y][x] = str(num)
            else:
                grid[size - 1 - y][x] = str(num // 10)
    
    for row in grid:
        print("  " + " ".join(row))


def test_lsystem():
    """Test the L-system generation"""
    print("L-System Generation Test:")
    print("-" * 40)
    
    for iterations in range(1, 4):
        lstring = generate_moore_curve_lsystem(iterations)
        print(f"Iteration {iterations}: {lstring[:50]}{'...' if len(lstring) > 50 else ''}")
        print(f"Length: {len(lstring)}")


def main():
    """Main function to demonstrate Moore curve visualizations"""
    print("Moore Curve Path Visualizer")
    print("=" * 60)
    
    # Test L-system
    test_lsystem()
    
    # Test different grid sizes
    sizes = [2, 3, 4, 5, 6]
    
    for size in sizes:
        if size <= 4:
            # Detailed visualization for small grids
            print_moore_curve(size)
        else:
            # Simple visualization for larger grids
            print_moore_curve_simple(size)
    
    # Test the path generation function from harvest_single
    print(f"\n{'='*60}")
    print("Testing get_next_dino() function:")
    print(f"{'='*60}")
    
    # Simulate the get_next_dino function behavior
    try:
        from harvest_single import get_next_dino
        
        # Test with a 4x4 grid
        size = 4
        print(f"\nSimulating dino movement on {size}x{size} grid:")
        
        # Generate path using our function
        path = generate_moore_curve_path(size)
        print(f"Generated path: {path[:10]}...")
        
        # Test path coverage
        all_positions = [(x, y) for x in range(size) for y in range(size)]
        covered = set(path)
        missing = set(all_positions) - covered
        
        print(f"Covered positions: {len(covered)}/{len(all_positions)}")
        if missing:
            print(f"Missing positions: {sorted(missing)}")
        else:
            print("All positions covered!")
            
    except ImportError as e:
        print(f"Could not import get_next_dino: {e}")


if __name__ == "__main__":
    main()
