# FastBox – Mystery Delivery System

## Overview
This project simulates one day of package deliveries by assigning each package to the nearest delivery agent using Euclidean distance.
For each delivery, the agent travels from its location to the warehouse and then to the destination.
The program generates a delivery report showing packages delivered, total distance traveled, efficiency per agent, and the most efficient agent.
The report is printed to the console and also saved to `report.json`.
Assumptions are documented in code comments for ambiguous scenarios.
Bonus features include simulated delivery delays, ASCII route visualization, mid-day agent addition, and CSV export of the top-performing agent.
All bonus logic is optional, deterministic, and isolated from core simulation logic.

## Assumptions
1. Agents start from their original location for every package.
2. Distance is calculated using Euclidean distance.
3. Each package is delivered independently.
4. If multiple agents are equidistant, the agent with the smallest ID is chosen.
5. Efficiency = total_distance / packages_delivered.
6. Input JSON is assumed to be valid.

## How to Run
```bash
python delivery_simulator.py
