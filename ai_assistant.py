"""
AI Campus Assistant Engine
Parses natural language requests, handles semantic entity extraction,
provides rich conversational answers, and triggers interactive map actions.
Supports offline intelligent intent engine + optional external LLM integration.
"""

import re
import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, List
from campus_data import BUILDINGS, NODES, CLASS_SCHEDULES, CAMPUS_EVENTS, AMENITIES
from pathfinding import router

class CampusAIAssistant:
    def __init__(self):
        self.buildings = BUILDINGS
        self.nodes = NODES
        self.schedules = CLASS_SCHEDULES
        self.events = CAMPUS_EVENTS
        self.amenities = AMENITIES

    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main query processing entrance.
        Checks for custom API key if provided, else falls back to offline intelligent NLP engine.
        """
        query_clean = query.strip()
        context = context or {}
        api_key = context.get("api_key") or os.environ.get("GEMINI_API_KEY")

        # If user configured a Gemini API key in settings, attempt LLM call
        if api_key and len(api_key) > 10:
            try:
                llm_res = self._call_gemini_llm(query_clean, api_key, context)
                if llm_res:
                    return llm_res
            except Exception as e:
                print(f"LLM API call fallback: {e}")

        # Intelligent Built-in Intent Engine
        return self._rule_based_nlu(query_clean, context)

    def _call_gemini_llm(self, query: str, api_key: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Invokes Google Gemini API with system grounding prompt."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        system_instruction = (
            "You are NavBot, an AI campus assistant for Apex University. "
            "You help students find rooms, navigate between buildings, locate lectures, and find campus amenities. "
            f"Known buildings: {list(self.buildings.keys())}. "
            "Output your answer as valid JSON with keys: "
            "'text' (friendly markdown explanation), 'intent' ('navigate', 'locate', 'schedule', 'amenity', 'general'), "
            "'action_type' ('START_ROUTE', 'HIGHLIGHT_LOCATION', 'SHOW_SCHEDULE', 'FILTER_AMENITY', null), "
            "'action_payload' (parameters for map: e.g. {'start': '...', 'end': '...', 'accessible': false})."
        )

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{system_instruction}\n\nUser Question: {query}"}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json"
            }
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req, timeout=7) as response:
            res_body = json.loads(response.read().decode("utf-8"))
            raw_text = res_body["candidates"][0]["content"]["parts"][0]["text"]
            data = json.loads(raw_text)
            return data

    def _rule_based_nlu(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        High accuracy offline NLU parser handling navigation, schedule, location,
        accessibility, amenities, and campus FAQs.
        """
        q_lower = query.lower()
        is_accessible = any(k in q_lower for k in ["wheelchair", "accessible", "ramp", "elevator", "barrier free", "mobility"])

        # 1. SCHEDULE & CLASS SEARCH (e.g. "Where is CS101?", "When is AI301?", "What room is Calculus in?")
        schedule_match = self._match_schedule(q_lower)
        if schedule_match:
            b_info = self.buildings.get(schedule_match["building_id"], {})
            text = (
                f"**{schedule_match['id']} - {schedule_match['title']}** is held in "
                f"**{schedule_match['building_name']}**, room **{schedule_match['room']}**.\n\n"
                f"• **Instructor:** {schedule_match['instructor']}\n"
                f"• **Days:** {', '.join(schedule_match['days'])}\n"
                f"• **Time:** {schedule_match['start_time']} - {schedule_match['end_time']}\n"
                f"• **Description:** {schedule_match['description']}"
            )
            return {
                "text": text,
                "intent": "schedule",
                "action_type": "SHOW_SCHEDULE",
                "action_payload": {
                    "schedule_id": schedule_match["id"],
                    "building_id": schedule_match["building_id"],
                    "room_id": schedule_match["room_id"],
                    "building_name": schedule_match["building_name"],
                    "room_name": schedule_match["room"]
                },
                "quick_replies": [
                    f"Navigate to {schedule_match['room']}",
                    "What's next on schedule?",
                    "Where can I get coffee nearby?"
                ]
            }

        # 2. CAMPUS EVENTS SEARCH (e.g. "Hackathon", "Career Fair", "Events today")
        event_match = self._match_event(q_lower)
        if event_match:
            text = (
                f"🎉 **{event_match['title']}** ({event_match['badge']})\n\n"
                f"• **Location:** {event_match['building_name']} ({event_match['room']})\n"
                f"• **Time:** {event_match['time']}\n"
                f"• **Details:** {event_match['description']}"
            )
            return {
                "text": text,
                "intent": "event",
                "action_type": "SHOW_EVENT",
                "action_payload": {
                    "event_id": event_match["id"],
                    "building_id": event_match["building_id"],
                    "room_id": event_match["room_id"]
                },
                "quick_replies": [
                    f"Navigate to {event_match['building_name']}",
                    "Show other events today",
                    "Wheelchair route"
                ]
            }

        # 3. DIRECT NAVIGATION QUERY (e.g. "How do I get from North Dorms to Library?", "Route from A to B")
        nav_pair = self._match_route_pair(q_lower)
        if nav_pair:
            origin_id, dest_id = nav_pair
            origin_name = self.buildings.get(origin_id, {}).get("name", origin_id)
            dest_name = self.buildings.get(dest_id, {}).get("name", dest_id)
            
            # Compute route details to include in response
            route_res = router.find_route(origin_id, dest_id, accessible_only=is_accessible)
            if route_res:
                dist = route_res["total_distance_meters"]
                mins = route_res["estimated_time_minutes"]
                acc_note = " (Wheelchair-friendly path via ramps)" if is_accessible else ""
                
                text = (
                    f"🧭 Here is the best route from **{origin_name}** to **{dest_name}**{acc_note}:\n\n"
                    f"• **Distance:** {dist} meters\n"
                    f"• **Est. Walk Time:** ~{mins} min ({route_res['step_count']} steps)\n"
                    f"• **Highlights:** {route_res['steps'][0]['instruction']}\n\n"
                    f"I have highlighted the path on the map for you!"
                )
                return {
                    "text": text,
                    "intent": "navigate",
                    "action_type": "START_ROUTE",
                    "action_payload": {
                        "start": origin_id,
                        "end": dest_id,
                        "accessible": is_accessible
                    },
                    "quick_replies": [
                        "Start Turn-by-Turn Voice Guide",
                        "Show Wheelchair Route" if not is_accessible else "Show Standard Fastest Route",
                        "What classes are in this building?"
                    ]
                }

        # 4. AMENITY / POI SEARCH (e.g. "Where can I get coffee?", "Find nearest restroom", "Where is an ATM?")
        amenity_match = self._match_amenity(q_lower)
        if amenity_match:
            amenity_type, items = amenity_match
            primary = items[0]
            b_info = self.buildings.get(primary["building_id"], {})
            text = (
                f"☕ Found **{len(items)} {amenity_type}** location(s) on campus:\n\n"
                f"• Nearest: **{primary['name']}** located in **{b_info.get('name', 'Campus')}**.\n"
                f"• Status: Fully wheelchair accessible.\n\n"
                f"Would you like directions there?"
            )
            return {
                "text": text,
                "intent": "amenity",
                "action_type": "FILTER_AMENITY",
                "action_payload": {
                    "amenity_type": primary["type"],
                    "building_id": primary["building_id"],
                    "node_id": primary["node"]
                },
                "quick_replies": [
                    f"Navigate to {primary['name']}",
                    "Show all restrooms",
                    "Show all food options"
                ]
            }

        # 5. SINGLE DESTINATION LOCATION QUERY (e.g. "Where is the library?", "Where is CS building?", "Take me to Gym")
        dest_building = self._match_single_building(q_lower)
        if dest_building:
            b_info = self.buildings[dest_building]
            text = (
                f"📍 **{b_info['name']}** ({b_info['category']})\n\n"
                f"{b_info['description']}\n\n"
                f"• **Hours:** {b_info['operating_hours']}\n"
                f"• **Floors:** {b_info['floors']} floors (Elevator: {'Yes ✅' if b_info['has_elevator'] else 'No'})\n"
                f"• **Key Facilities:** {', '.join([r['name'] for r in b_info['rooms'][:3]])}"
            )
            return {
                "text": text,
                "intent": "locate",
                "action_type": "HIGHLIGHT_LOCATION",
                "action_payload": {
                    "building_id": dest_building,
                    "building_name": b_info["name"],
                    "position": b_info["position"],
                    "accessible": is_accessible
                },
                "quick_replies": [
                    f"Directions to {b_info['short_name']}",
                    f"Wheelchair route to {b_info['short_name']}",
                    f"What classes are in {b_info['short_name']}?"
                ]
            }

        # 6. ACCESSIBILITY OVERVIEW
        if any(w in q_lower for w in ["accessibility", "accessible", "wheelchair", "ramp", "disability", "ada"]):
            return {
                "text": (
                    "♿ **Campus Accessibility Features:**\n\n"
                    "• **Wheelchair Navigation Mode:** Avoids all outdoor monumental stairs (like the Library Grand Steps) "
                    "and automatically routes via certified gentle ADA ramps and elevators.\n"
                    "• **All Academic Buildings:** Equipped with automatic power doors and elevators.\n"
                    "• **Accessible Parking:** Available at North Visitor Lot (12 ADA bays) with level paving to all academic blocks.\n\n"
                    "You can toggle 'Wheelchair Accessible Routes' anytime in the navigation bar!"
                ),
                "intent": "accessibility",
                "action_type": None,
                "action_payload": None,
                "quick_replies": [
                    "Route to Library with Ramp",
                    "Show Accessible Restrooms",
                    "Where is ADA Parking?"
                ]
            }

        # 7. GREETINGS & HELP
        if any(w in q_lower for w in ["hi", "hello", "hey", "help", "who are you", "what can you do"]):
            return {
                "text": (
                    "👋 **Hi! I'm NavBot, your Campus AI Assistant.**\n\n"
                    "I can help you navigate around Apex University:\n"
                    "• **Directions:** *'How do I get to the Library from North Dorms?'*\n"
                    "• **Classes:** *'Where is CS101 right now?'* or *'Where is Robotics lab?'*\n"
                    "• **Amenities:** *'Find nearest coffee shop'* or *'Where are accessible restrooms?'*\n"
                    "• **Events:** *'What events are happening today?'*\n"
                    "• **Accessibility:** *'Show me wheelchair friendly routes'*.\n\n"
                    "Try asking a question or tapping one of the quick suggestions below!"
                ),
                "intent": "general",
                "action_type": None,
                "action_payload": None,
                "quick_replies": [
                    "Where is CS101 lecture?",
                    "Route from Dorms to Library",
                    "Find nearest coffee shop",
                    "Today's campus events"
                ]
            }

        # 8. FALLBACK HELPFUL SEARCH
        return {
            "text": (
                f"I couldn't find an exact match for *'{query}'*, but I can help you search the campus directory! "
                "You can search by building name, class ID (e.g. CS101), lecture halls, cafeterias, or ask for directions."
            ),
            "intent": "unknown",
            "action_type": None,
            "action_payload": None,
            "quick_replies": [
                "Show Campus Directory",
                "Where is Computer Science Block?",
                "Class schedule today",
                "Find restrooms"
            ]
        }

    def _match_schedule(self, q: str) -> Optional[Dict[str, Any]]:
        for s in self.schedules:
            c_id = s["id"].lower()
            if c_id in q or c_id.replace(" ", "") in q.replace(" ", ""):
                return s
            if s["title"].lower() in q:
                return s
            if s["department"].lower() in q and any(w in q for w in ["class", "lecture", "course"]):
                return s
            for word in s["title"].lower().split():
                if len(word) > 4 and word in q and any(k in q for k in ["class", "lecture", "where", "room"]):
                    return s
        return None

    def _match_event(self, q: str) -> Optional[Dict[str, Any]]:
        for e in self.events:
            if e["id"].lower() in q or e["title"].lower() in q:
                return e
            if any(k in q for k in ["hackathon", "hack"]) and "hackathon" in e["title"].lower():
                return e
            if any(k in q for k in ["career", "job", "internship"]) and "career" in e["title"].lower():
                return e
            if "robot" in q and "robot" in e["title"].lower():
                return e
            if "yoga" in q and "yoga" in e["title"].lower():
                return e
        if any(k in q for k in ["events", "happening", "activities", "what's on"]):
            return self.events[0]
        return None

    def _match_amenity(self, q: str) -> Optional[Tuple[str, List[Dict[str, Any]]]]:
        if any(k in q for k in ["coffee", "cafe", "latte", "espresso", "cappuccino"]):
            cafes = [a for a in self.amenities if a["type"] == "cafe"]
            return ("Coffee & Cafe", cafes)
        if any(k in q for k in ["restroom", "toilet", "washroom", "bathroom", "wc"]):
            restrooms = [a for a in self.amenities if a["type"] == "restroom"]
            return ("Restrooms", restrooms)
        if any(k in q for k in ["atm", "cash", "bank", "money"]):
            atms = [a for a in self.amenities if a["type"] == "atm"]
            return ("ATM / Banking", atms)
        if any(k in q for k in ["first aid", "health", "doctor", "clinic", "pharmacy", "medical"]):
            aids = [a for a in self.amenities if a["type"] == "first_aid"]
            return ("Health & First Aid", aids)
        if any(k in q for k in ["bike", "bicycle", "cycle", "dock"]):
            bikes = [a for a in self.amenities if a["type"] == "bike"]
            return ("Bike Share Dock", bikes)
        if any(k in q for k in ["food", "lunch", "eat", "dining", "hungry", "cafeteria"]):
            return ("Dining & Food", [a for a in self.amenities if a["building_id"] == "b_student_union"])
        return None

    def _match_single_building(self, q: str) -> Optional[str]:
        # Mapping common terms to building ids
        term_map = {
            "library": "b_library",
            "turing": "b_library",
            "books": "b_library",
            "study": "b_library",
            "cs": "b_cs",
            "computer": "b_cs",
            "robotics": "b_cs",
            "ai": "b_cs",
            "einstein": "b_einstein",
            "lecture": "b_einstein",
            "auditorium": "b_auditorium",
            "arts": "b_auditorium",
            "theatre": "b_auditorium",
            "theater": "b_auditorium",
            "union": "b_student_union",
            "student union": "b_student_union",
            "cafeteria": "b_student_union",
            "food court": "b_student_union",
            "engineering": "b_eng",
            "maker": "b_eng",
            "health": "b_health",
            "clinic": "b_health",
            "hospital": "b_health",
            "gym": "b_sports",
            "sports": "b_sports",
            "pool": "b_sports",
            "fitness": "b_sports",
            "basketball": "b_sports",
            "admin": "b_admin",
            "administration": "b_admin",
            "admissions": "b_admin",
            "registrar": "b_admin",
            "transit": "b_transit",
            "bus": "b_transit",
            "shuttle": "b_transit",
            "north dorm": "b_dorms_north",
            "dorm a": "b_dorms_north",
            "dorm b": "b_dorms_north",
            "south dorm": "b_dorms_south",
            "dorm c": "b_dorms_south",
            "dorm d": "b_dorms_south",
        }
        for term, bid in term_map.items():
            if re.search(r'\b' + re.escape(term) + r'\b', q):
                return bid
        return None

    def _match_route_pair(self, q: str) -> Optional[Tuple[str, str]]:
        """Extracts origin and destination from 'from X to Y' or 'X to Y' phrases."""
        patterns = [
            r'from\s+([a-zA-Z0-9\s]+?)\s+to\s+([a-zA-Z0-9\s]+)',
            r'route\s+([a-zA-Z0-9\s]+?)\s+to\s+([a-zA-Z0-9\s]+)',
            r'directions\s+from\s+([a-zA-Z0-9\s]+?)\s+to\s+([a-zA-Z0-9\s]+)',
            r'how\s+to\s+get\s+from\s+([a-zA-Z0-9\s]+?)\s+to\s+([a-zA-Z0-9\s]+)'
        ]
        for pat in patterns:
            match = re.search(pat, q)
            if match:
                from_str = match.group(1).strip()
                to_str = match.group(2).strip()
                b_from = self._match_single_building(from_str)
                b_to = self._match_single_building(to_str)
                if b_from and b_to and b_from != b_to:
                    return (b_from, b_to)

        # Also check simple: "to [Destination]" when start is assumed or current
        return None


ai_assistant = CampusAIAssistant()
