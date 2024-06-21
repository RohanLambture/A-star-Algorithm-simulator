# A* Path Finding Algorithm Simulator

An interactive simulation project that visualizes the A* pathfinding algorithm.

## Overview

This project demonstrates the A* pathfinding algorithm in an interactive and visual manner. It allows users to create a grid, set start and end points, place barriers, and watch the algorithm find the shortest path. The simulation is implemented using Python and Pygame, providing a user-friendly interface and dynamic visual feedback.

## Features

- **Interactive Grid Creation**: Users can create a grid and place barriers to simulate different scenarios.
- **Dynamic Options Panel**: Includes buttons for selecting start and end points, setting barriers, and resetting the grid.
- **Visual Pathfinding**: The algorithm's progress is displayed in real-time, with different colors representing different states of the nodes (e.g., open, closed, path).
- **User Controls**: Start, end, wall, and ground placement, along with start and reset buttons for the simulation.

## Tech Stack

- **Python**: Core programming language used.
- **Pygame**: Library used for creating the interactive simulation and user interface.

## How It Works

1. **Grid Setup**: The grid is created with an options panel on the left and a drawing area on the right.
2. **Tool Selection**: Users can select tools from the options panel to set the start point, end point, barriers, or reset nodes to the ground.
3. **Pathfinding**: Once the start and end points are set, users can initiate the A* algorithm by clicking the "Start" button or pressing the spacebar.
4. **Visualization**: The algorithm visualizes the pathfinding process, showing the open, closed, and path nodes in different colors.
5. **Reset**: The grid can be reset using the "Reset" button or pressing the "C" key to clear the grid and start over.

## Installation and Usage

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/a-star-pathfinding-simulator.git
    cd a-star-pathfinding-simulator
    ```

2. **Install Dependencies**:
    ```bash
    pip install pygame
    ```

3. **Run the Simulation**:
    ```bash
    python main.py
    ```

## User Guide

- **Left Click**:
  - On the options panel to select tools (start, end, wall, ground).
  - On the grid to place the selected tool's node.
- **Right Click**: On the grid to reset a node to the ground state.
- **Spacebar**: Start the A* algorithm if start and end points are set.
- **C Key**: Clear the grid.
- **Buttons**: Use the "Start" button to initiate the pathfinding and the "Reset" button to clear the grid.

