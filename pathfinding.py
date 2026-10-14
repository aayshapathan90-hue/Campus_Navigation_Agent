"""
Pathfinding Engine for Campus Navigation Assistant
Implements A* and Dijkstra algorithms with multi-criteria accessibility routing
and rich turn-by-turn guidance generation.
"""

import math
import heapq
from typing import Dict, List, Tuple, Any, Optional
from campus_data import NODES, EDGES, BUILDINGS

class CampusRouter:
    def __init__(self):
        self.nodes = NODES
        self.edges = EDGES
        self.buildings = BUILDINGS
        self.graph = self._build_adjacency_list()

    def _build_adjacency_list(self) -> Dict[str, List[Dict[str, Any]]]:
        """Constructs an undirected adjacency list from EDGES."""
        adj: Dict[str, List[Dict[str, Any]]] = {nid: [] for nid in self.nodes}
        for edge in self.edges:
            u, v = edge["u"], edge["v"]
            weight = edge.get("weight", 50)
            accessible = edge.get("accessible", True)
            stairs = edge.get("stairs", False)
            surface = edge.get("surface", "Paved Walkway")
            name = edge.get("name", "")

            if u in adj and v in adj:
                adj[u].append({
                    "to": v,
                    "weight": weight,
                    "accessible": accessible,
                    "stairs": stairs,
                    "surface": surface,
                    "name": name
                })
                adj[v].append({
                    "to": u,
                    "weight": weight,
                    "accessible": accessible,
                    "stairs": stairs,
                    "surface": surface,
                    "name": name
                })
        return adj

    def _heuristic(self, node_a: str, node_b: str) -> float:
        """Euclidean distance heuristic between two nodes in map units."""
        pos_a = self.nodes[node_a]["pos"]
        pos_b = self.nodes[node_b]["pos"]
        # pos is [y, x]
        dy = pos_a[0] - pos_b[0]
        dx = pos_a[1] - pos_b[1]
        return math.hypot(dx, dy)

    def find_route(
        self,
        start_id: str,
        end_id: str,
        accessible_only: bool = False,
        algorithm: str = "astar"
    ) -> Optional[Dict[str, Any]]:
        """
        Find the optimal route between start_id and end_id.
        IDs can be building IDs (e.g. 'b_cs') or node IDs (e.g. 'n_cs_ent').
        """
        start_node = self._resolve_to_node(start_id)
        end_node = self._resolve_to_node(end_id)

        if not start_node or not end_node:
            return None

        if start_node == end_node:
            node_info = self.nodes[start_node]
            return {
                "path_nodes": [start_node],
                "coordinates": [node_info["pos"]],
                "total_distance": 0,
                "estimated_time_seconds": 0,
                "accessible": True,
                "steps": [
                    {
                        "step_number": 1,
                        "instruction": f"You are already at {node_info['name']}.",
                        "distance": 0,
                        "action": "arrive",
                        "accessible": True
                    }
                ]
            }

        # Check start/end node accessibility requirement
        if accessible_only:
            if not self.nodes[start_node].get("accessible", True) or not self.nodes[end_node].get("accessible", True):
                return None

        # Priority queue stores tuples: (priority, current_cost, current_node, path_history, edge_history)
        # using A* or Dijkstra
        pq = []
        start_h = self._heuristic(start_node, end_node) if algorithm == "astar" else 0
        heapq.heappush(pq, (start_h, 0, start_node, [start_node], []))

        best_cost = {start_node: 0}

        while pq:
            est_total, current_cost, current_node, path_nodes, edge_history = heapq.heappop(pq)

            if current_node == end_node:
                # Target reached!
                return self._build_route_result(path_nodes, edge_history, current_cost, accessible_only)

            if current_cost > best_cost.get(current_node, float("inf")):
                continue

            for neighbor in self.graph.get(current_node, []):
                next_node = neighbor["to"]
                is_accessible = neighbor.get("accessible", True)
                is_stairs = neighbor.get("stairs", False)

                # Filter if accessible_only mode is on
                if accessible_only:
                    if not is_accessible or is_stairs:
                        continue
                    if not self.nodes[next_node].get("accessible", True):
                        continue

                new_cost = current_cost + neighbor["weight"]
                if new_cost < best_cost.get(next_node, float("inf")):
                    best_cost[next_node] = new_cost
                    priority = new_cost + (self._heuristic(next_node, end_node) if algorithm == "astar" else 0)
                    heapq.heappush(
                        pq,
                        (priority, new_cost, next_node, path_nodes + [next_node], edge_history + [neighbor])
                    )

        # No path found
        return None

    def _resolve_to_node(self, identifier: str) -> Optional[str]:
        """Resolves building ID, room ID, or node ID to a valid graph node ID."""
        if identifier in self.nodes:
            return identifier
        
        if identifier in self.buildings:
            return self.buildings[identifier]["entrance_node"]

        # Search inside rooms
        for b_id, b_data in self.buildings.items():
            for room in b_data.get("rooms", []):
                if room.get("id") == identifier or room.get("name", "").lower() == identifier.lower():
                    return b_data["entrance_node"]

        # Fallback case-insensitive match on building names
        for b_id, b_data in self.buildings.items():
            if identifier.lower() in b_data["name"].lower() or identifier.lower() in b_data["short_name"].lower():
                return b_data["entrance_node"]

        # Fallback node name match
        for n_id, n_data in self.nodes.items():
            if identifier.lower() in n_data["name"].lower():
                return n_id

        return None

    def _build_route_result(
        self,
        path_nodes: List[str],
        edge_history: List[Dict[str, Any]],
        total_distance: float,
        accessible_only: bool
    ) -> Dict[str, Any]:
        """Constructs detailed path result, turn-by-turn guidance, and navigation metrics."""
        coords = [self.nodes[nid]["pos"] for nid in path_nodes]
        
        # Walking speed: 1.2 m/s standard (~4.3 km/h), 1.0 m/s for wheelchair/slow pace
        speed = 1.0 if accessible_only else 1.2
        walk_time_sec = int(total_distance / speed)
        calories = round(total_distance * 0.045, 1)
        steps = int(total_distance * 1.35)

        turn_by_turn = self._generate_turn_by_turn(path_nodes, edge_history)

        return {
            "path_nodes": path_nodes,
            "coordinates": coords,
            "total_distance_meters": round(total_distance, 1),
            "estimated_time_seconds": walk_time_sec,
            "estimated_time_minutes": max(1, math.ceil(walk_time_sec / 60)),
            "calories_burned": calories,
            "step_count": steps,
            "is_accessible": accessible_only,
            "has_stairs": any(e.get("stairs", False) for e in edge_history),
            "steps": turn_by_turn
        }

    def _generate_turn_by_turn(
        self,
        path_nodes: List[str],
        edge_history: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generates natural language turn-by-turn steps with landmark context."""
        if not path_nodes or len(path_nodes) < 2:
            return []

        steps = []
        start_node_info = self.nodes[path_nodes[0]]
        first_edge = edge_history[0] if edge_history else {}
        first_dest_info = self.nodes[path_nodes[1]]

        # Initial departure instruction
        steps.append({
            "step_number": 1,
            "action": "depart",
            "instruction": f"Depart from {start_node_info['name']} along the {first_edge.get('surface', 'walkway')}.",
            "node_from": path_nodes[0],
            "node_to": path_nodes[1],
            "distance": first_edge.get("weight", 0),
            "accessible": first_edge.get("accessible", True),
            "stairs": first_edge.get("stairs", False)
        })

        for i in range(1, len(path_nodes) - 1):
            prev_nid = path_nodes[i - 1]
            curr_nid = path_nodes[i]
            next_nid = path_nodes[i + 1]
            edge = edge_history[i] if i < len(edge_history) else {}

            curr_info = self.nodes[curr_nid]
            next_info = self.nodes[next_nid]

            # Calculate turn angle
            p_prev = self.nodes[prev_nid]["pos"]
            p_curr = self.nodes[curr_nid]["pos"]
            p_next = self.nodes[next_nid]["pos"]

            # Vector 1: prev -> curr (Leaflet is [y, x], so dx = x1 - x0, dy = y1 - y0)
            v1_x = p_curr[1] - p_prev[1]
            v1_y = p_curr[0] - p_prev[0]

            # Vector 2: curr -> next
            v2_x = p_next[1] - p_curr[1]
            v2_y = p_next[0] - p_curr[0]

            angle = self._calculate_turn_angle(v1_x, v1_y, v2_x, v2_y)
            turn_direction, action_icon = self._classify_turn(angle)

            # Special landmark phrasing
            landmark_cue = ""
            if "ramp" in curr_info["name"].lower() or edge.get("surface", "").lower().find("ramp") >= 0:
                landmark_cue = " via the ADA Wheelchair Accessible Ramp"
            elif edge.get("stairs", False):
                landmark_cue = " using the Monumental Stone Steps (caution: stairs)"
            elif "fountain" in curr_info["name"].lower():
                landmark_cue = " past the Solar Fountain Plaza"

            instruction = f"{turn_direction} at {curr_info['name']}{landmark_cue} towards {next_info['name']} ({edge.get('weight', 0)}m)."

            steps.append({
                "step_number": len(steps) + 1,
                "action": action_icon,
                "turn": turn_direction,
                "angle": round(angle, 1),
                "instruction": instruction,
                "node_from": curr_nid,
                "node_to": next_nid,
                "distance": edge.get("weight", 0),
                "accessible": edge.get("accessible", True),
                "stairs": edge.get("stairs", False)
            })

        # Final arrival step
        dest_node_info = self.nodes[path_nodes[-1]]
        steps.append({
            "step_number": len(steps) + 1,
            "action": "arrive",
            "instruction": f"Arrive at destination: {dest_node_info['name']}.",
            "node_from": path_nodes[-1],
            "node_to": path_nodes[-1],
            "distance": 0,
            "accessible": dest_node_info.get("accessible", True),
            "stairs": False
        })

        return steps

    def _calculate_turn_angle(self, v1_x: float, v1_y: float, v2_x: float, v2_y: float) -> float:
        """Calculates signed angle between two vectors in degrees (-180 to +180)."""
        dot = v1_x * v2_x + v1_y * v2_y
        det = v1_x * v2_y - v1_y * v2_x  # 2D cross product
        angle_rad = math.atan2(det, dot)
        return math.degrees(angle_rad)

    def _classify_turn(self, angle: float) -> Tuple[str, str]:
        """Classifies angle into navigation phrasing."""
        if -25 <= angle <= 25:
            return "Continue straight", "straight"
        elif 25 < angle <= 65:
            return "Bear slight right", "slight-right"
        elif 65 < angle <= 125:
            return "Turn right", "turn-right"
        elif 125 < angle <= 180:
            return "Make a sharp right / U-turn", "sharp-right"
        elif -65 <= angle < -25:
            return "Bear slight left", "slight-left"
        elif -125 <= angle < -65:
            return "Turn left", "turn-left"
        else:
            return "Make a sharp left / U-turn", "sharp-left"


# Global router singleton
router = CampusRouter()
