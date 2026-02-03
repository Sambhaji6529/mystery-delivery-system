import json
import math
import random
import csv
from typing import Dict, Tuple


# -----------------------------
# Utility Functions
# -----------------------------

def euclidean_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two 2D points."""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def visualize_route(agent_id: str, warehouse_id: str, destination: Tuple[float, float]) -> None:
    """
    ASCII visualization of delivery route.
    Bonus feature.
    """
    print(f"Route: {agent_id} --> {warehouse_id} --> {destination}")


# -----------------------------
# Core Logic
# -----------------------------

def assign_nearest_agent(
    agents: Dict[str, Tuple[float, float]],
    warehouse_location: Tuple[float, float]
) -> str:
    """
    Assign the nearest agent to a warehouse.
    
    Assumption:
    - If two agents are at equal distance, choose lexicographically smaller agent ID.
    """
    nearest_agent = None
    min_distance = float("inf")

    for agent_id, agent_location in agents.items():
        distance = euclidean_distance(agent_location, warehouse_location)

        if distance < min_distance:
            min_distance = distance
            nearest_agent = agent_id
        elif distance == min_distance and agent_id < nearest_agent:
            nearest_agent = agent_id

    return nearest_agent


def simulate_delivery(data: Dict) -> Dict:
    """
    Simulates one day of deliveries.

    Assumptions:
    - Agents start from their original position for every package.
    - Each package is delivered independently.
    - Random delivery delay between 0–10 minutes (bonus).
    - A new agent joins mid-day (bonus).
    """

    random.seed(42)  # deterministic randomness for evaluation

    warehouses = {k: tuple(v) for k, v in data["warehouses"].items()}
    agents = {k: tuple(v) for k, v in data["agents"].items()}
    packages = data["packages"]

    report = {
        agent_id: {
            "packages_delivered": 0,
            "total_distance": 0.0,
            "total_delay": 0
        }
        for agent_id in agents
    }

    mid_point = len(packages) // 2

    for index, package in enumerate(packages):

        # Bonus: new agent joins mid-day
        if index == mid_point:
            agents["AX"] = (0, 0)
            report["AX"] = {
                "packages_delivered": 0,
                "total_distance": 0.0,
                "total_delay": 0
            }
            print("New agent AX joined mid-day at location (0,0)")

        warehouse_id = package["warehouse"]
        destination = tuple(package["destination"])
        warehouse_location = warehouses[warehouse_id]

        assigned_agent = assign_nearest_agent(agents, warehouse_location)
        agent_location = agents[assigned_agent]

        # Distance calculation
        distance_to_warehouse = euclidean_distance(agent_location, warehouse_location)
        distance_to_destination = euclidean_distance(warehouse_location, destination)
        total_distance = distance_to_warehouse + distance_to_destination

        # Bonus: random delivery delay
        delay_minutes = random.randint(0, 10)

        # Update report
        report[assigned_agent]["packages_delivered"] += 1
        report[assigned_agent]["total_distance"] += total_distance
        report[assigned_agent]["total_delay"] += delay_minutes

        # Bonus: ASCII route visualization
        visualize_route(assigned_agent, warehouse_id, destination)

    # Compute efficiency
    for agent_id, stats in report.items():
        if stats["packages_delivered"] > 0:
            stats["efficiency"] = round(
                stats["total_distance"] / stats["packages_delivered"], 2
            )
        else:
            stats["efficiency"] = None

        stats["total_distance"] = round(stats["total_distance"], 2)

    return report


def find_most_efficient_agent(report: Dict) -> str:
    """Return agent with the lowest efficiency score."""
    return min(
        (a for a in report if report[a]["efficiency"] is not None),
        key=lambda x: report[x]["efficiency"]
    )


def export_best_agent_to_csv(agent_id: str, report: Dict) -> None:
    """
    Bonus feature:
    Export top-performing agent to CSV.
    """
    with open("top_agent.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Agent", "Packages Delivered", "Total Distance", "Efficiency"])
        writer.writerow([
            agent_id,
            report[agent_id]["packages_delivered"],
            report[agent_id]["total_distance"],
            report[agent_id]["efficiency"]
        ])


# -----------------------------
# Entry Point
# -----------------------------

def main():
    with open("data.json", "r") as file:
        data = json.load(file)

    report = simulate_delivery(data)
    best_agent = find_most_efficient_agent(report)

    print("\nDelivery Report:")
    for agent, stats in report.items():
        print(f"{agent}: {stats}")

    print(f"\nMost Efficient Agent: {best_agent}")

    # Save report to JSON (required)
    with open("report.json", "w") as f:
        json.dump(
            {
                **report,
                "best_agent": best_agent
            },
            f,
            indent=2
        )

    # Bonus: export best agent to CSV
    export_best_agent_to_csv(best_agent, report)


if __name__ == "__main__":
    main()
