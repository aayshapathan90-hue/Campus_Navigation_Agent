"""
Flask Web Application for Campus Navigation Assistant
Serves RESTful APIs and interactive Web UI.
"""

from flask import Flask, render_template, jsonify, request
from campus_data import (
    CAMPUS_CONFIG,
    BUILDINGS,
    LANDMARKS,
    NODES,
    EDGES,
    CLASS_SCHEDULES,
    CAMPUS_EVENTS,
    AMENITIES
)
from pathfinding import router
from ai_assistant import ai_assistant

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/campus", methods=["GET"])
def get_campus():
    """Returns static campus layout, buildings, graph, and amenities."""
    return jsonify({
        "config": CAMPUS_CONFIG,
        "buildings": list(BUILDINGS.values()),
        "landmarks": LANDMARKS,
        "nodes": NODES,
        "edges": EDGES,
        "amenities": AMENITIES
    })

@app.route("/api/route", methods=["POST"])
def get_route():
    """
    Computes shortest path between two points.
    Payload: { "start": str, "end": str, "accessible": bool, "algorithm": "astar"|"dijkstra" }
    """
    data = request.get_json(force=True) or {}
    start_id = data.get("start")
    end_id = data.get("end")
    accessible_only = bool(data.get("accessible", False))
    algorithm = data.get("algorithm", "astar")

    if not start_id or not end_id:
        return jsonify({"error": "Both 'start' and 'end' parameters are required."}), 400

    route = router.find_route(start_id, end_id, accessible_only=accessible_only, algorithm=algorithm)
    if not route:
        # If accessible path failed, check if standard path exists to inform user
        if accessible_only:
            fallback = router.find_route(start_id, end_id, accessible_only=False)
            if fallback:
                return jsonify({
                    "error": "No completely stair-free accessible route found between these locations, but a standard pedestrian route is available.",
                    "accessible_available": False,
                    "standard_route": fallback
                }), 404
        return jsonify({"error": "No path could be found between the selected locations."}), 404

    return jsonify({"success": True, "route": route})

@app.route("/api/search", methods=["GET"])
def search_campus():
    """Search query across buildings, rooms, schedules, and amenities."""
    q = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "all").strip().lower()

    if not q and category == "all":
        # Return all buildings by default
        return jsonify({
            "results": [{"type": "building", "data": b} for b in BUILDINGS.values()]
        })

    results = []

    # Search buildings
    for b in BUILDINGS.values():
        if category in ["all", "academic", "dining", "admin", "housing"]:
            match_name = q in b["name"].lower() or q in b["short_name"].lower()
            match_cat = q in b["category"].lower()
            match_desc = q in b["description"].lower()
            if not q or match_name or match_cat or match_desc:
                results.append({"type": "building", "data": b})

        # Search rooms inside building
        for room in b.get("rooms", []):
            if not q or q in room["name"].lower() or q in room["id"].lower():
                results.append({
                    "type": "room",
                    "building_id": b["id"],
                    "building_name": b["name"],
                    "data": room
                })

    # Search courses & schedules
    if category in ["all", "classes"]:
        for c in CLASS_SCHEDULES:
            if not q or q in c["id"].lower() or q in c["title"].lower() or q in c["instructor"].lower():
                results.append({"type": "class", "data": c})

    # Search amenities
    if category in ["all", "amenities"]:
        for a in AMENITIES:
            if not q or q in a["name"].lower() or q in a["type"].lower():
                results.append({"type": "amenity", "data": a})

    return jsonify({"query": q, "results": results})

@app.route("/api/schedule", methods=["GET"])
def get_schedule():
    """Returns today's classes and campus events."""
    return jsonify({
        "classes": CLASS_SCHEDULES,
        "events": CAMPUS_EVENTS
    })

@app.route("/api/chat", methods=["POST"])
def chat_assistant():
    """Natural language AI query assistant."""
    data = request.get_json(force=True) or {}
    message = data.get("message", "").strip()
    context = data.get("context", {})

    if not message:
        return jsonify({"error": "Empty message"}), 400

    response = ai_assistant.process_query(message, context=context)
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
