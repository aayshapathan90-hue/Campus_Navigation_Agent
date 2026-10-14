"""
Campus Data Module for Campus Navigation Assistant
Defines campus graph (nodes, edges, buildings, amenities, schedules, and events).
"""

from typing import Dict, List, Any, Optional

# Campus bounds in coordinate units [x: 0..1000, y: 0..800]
CAMPUS_CONFIG = {
    "name": "Apex University & Technology Campus",
    "width": 1000,
    "height": 800,
    "center": [400, 500],
    "scale_label": "1 unit ≈ 1 meter"
}

# Building & Zone definitions
BUILDINGS: Dict[str, Dict[str, Any]] = {
    "b_admin": {
        "id": "b_admin",
        "name": "Administration & Chancellor Hall",
        "short_name": "Admin Building",
        "category": "Administration",
        "description": "Admissions, Registrar, Student Financial Services, Dean's Office",
        "position": [400, 150],  # [y, x] coordinate
        "polygon": [[360, 100], [360, 200], [440, 200], [440, 100]],
        "entrance_node": "n_admin_ent",
        "color": "#475569",
        "accent": "#94a3b8",
        "icon": "building",
        "accessible": True,
        "floors": 3,
        "has_elevator": True,
        "operating_hours": "08:30 - 17:00",
        "rooms": [
            {"id": "adm_101", "name": "Admissions Welcome Desk", "floor": 1, "accessible": True},
            {"id": "adm_102", "name": "Registrar Office", "floor": 1, "accessible": True},
            {"id": "adm_201", "name": "Dean of Students", "floor": 2, "accessible": True},
            {"id": "adm_205", "name": "Financial Aid & Bursar", "floor": 2, "accessible": True},
            {"id": "adm_301", "name": "Chancellor Boardroom", "floor": 3, "accessible": True}
        ]
    },
    "b_library": {
        "id": "b_library",
        "name": "Alan Turing Central Library",
        "short_name": "Library",
        "category": "Academic / Study",
        "description": "5-story central library with 24/7 study lounges, digital archives, and quiet pods",
        "position": [560, 360],
        "polygon": [[500, 300], [500, 420], [620, 420], [620, 300]],
        "entrance_node": "n_lib_ent",
        "color": "#1e40af",
        "accent": "#60a5fa",
        "icon": "book-open",
        "accessible": True,
        "floors": 5,
        "has_elevator": True,
        "operating_hours": "24/7 Study Hall, Stacks 08:00 - 23:00",
        "rooms": [
            {"id": "lib_desk", "name": "Circulation Desk & Help", "floor": 1, "accessible": True},
            {"id": "lib_cafe", "name": "Library Coffee Pod", "floor": 1, "accessible": True},
            {"id": "lib_201", "name": "Quiet Reading Hall", "floor": 2, "accessible": True},
            {"id": "lib_301", "name": "Digital Archives & VR Studio", "floor": 3, "accessible": True},
            {"id": "lib_401", "name": "Group Study Rooms 401-412", "floor": 4, "accessible": True}
        ]
    },
    "b_cs": {
        "id": "b_cs",
        "name": "Computer Science & AI Institute",
        "short_name": "CS Building",
        "category": "Academic",
        "description": "Faculty of CS, Artificial Intelligence labs, Cyber Security lab & Robotics",
        "position": [240, 350],
        "polygon": [[180, 290], [180, 410], [300, 410], [300, 290]],
        "entrance_node": "n_cs_ent",
        "color": "#0284c7",
        "accent": "#38bdf8",
        "icon": "cpu",
        "accessible": True,
        "floors": 4,
        "has_elevator": True,
        "operating_hours": "07:30 - 22:00",
        "rooms": [
            {"id": "cs_101", "name": "CS 101 Lecture Auditorium", "floor": 1, "accessible": True},
            {"id": "cs_105", "name": "Algorithms & Programming Lab", "floor": 1, "accessible": True},
            {"id": "cs_204", "name": "Deep Learning & Robotics Arena", "floor": 2, "accessible": True},
            {"id": "cs_301", "name": "Cybersecurity & Cloud Lab", "floor": 3, "accessible": True},
            {"id": "cs_401", "name": "Department Chair & Faculty Lounge", "floor": 4, "accessible": True}
        ]
    },
    "b_einstein": {
        "id": "b_einstein",
        "name": "Albert Einstein Lecture Halls Complex",
        "short_name": "Lecture Halls",
        "category": "Academic",
        "description": "Major stadium-seating auditoriums and amphitheater lecture rooms for core courses",
        "position": [240, 560],
        "polygon": [[180, 500], [180, 620], [300, 620], [300, 500]],
        "entrance_node": "n_einstein_ent",
        "color": "#7c3aed",
        "accent": "#a78bfa",
        "icon": "presentation",
        "accessible": True,
        "floors": 2,
        "has_elevator": True,
        "operating_hours": "08:00 - 20:00",
        "rooms": [
            {"id": "lh_1", "name": "Auditorium LH-1 (Grand)", "floor": 1, "accessible": True},
            {"id": "lh_2", "name": "Lecture Hall LH-2", "floor": 1, "accessible": True},
            {"id": "lh_3", "name": "Lecture Hall LH-3", "floor": 2, "accessible": True},
            {"id": "lh_amph", "name": "Chemistry Amphitheatre", "floor": 2, "accessible": True}
        ]
    },
    "b_eng": {
        "id": "b_eng",
        "name": "Engineering & Maker Innovation Hub",
        "short_name": "Engineering Hub",
        "category": "Academic",
        "description": "Mechanical, Electrical, 3D Prototyping MakerSpace, and Aerospace hangar",
        "position": [240, 780],
        "polygon": [[180, 710], [180, 850], [300, 850], [300, 710]],
        "entrance_node": "n_eng_ent",
        "color": "#d97706",
        "accent": "#fbbf24",
        "icon": "wrench",
        "accessible": True,
        "floors": 3,
        "has_elevator": True,
        "operating_hours": "08:00 - 22:00",
        "rooms": [
            {"id": "eng_maker", "name": "MakerSpace & 3D Print Lab", "floor": 1, "accessible": True},
            {"id": "eng_102", "name": "Circuits & Embedded Systems", "floor": 1, "accessible": True},
            {"id": "eng_205", "name": "Thermodynamics Lab", "floor": 2, "accessible": True},
            {"id": "eng_302", "name": "Senior Capstone Design Studio", "floor": 3, "accessible": True}
        ]
    },
    "b_student_union": {
        "id": "b_student_union",
        "name": "Campus Student Union & Food Pavilion",
        "short_name": "Student Union & Dining",
        "category": "Dining / Student Life",
        "description": "Dining hall, artisan coffee, campus bookstore, student government & gaming lounge",
        "position": [400, 560],
        "polygon": [[340, 500], [340, 620], [460, 620], [460, 500]],
        "entrance_node": "n_union_ent",
        "color": "#059669",
        "accent": "#34d399",
        "icon": "utensils",
        "accessible": True,
        "floors": 2,
        "has_elevator": True,
        "operating_hours": "07:00 - 23:00",
        "rooms": [
            {"id": "din_main", "name": "Apex Food Court & Global Kitchen", "floor": 1, "accessible": True},
            {"id": "din_cafe", "name": "The Daily Grind Espresso Bar", "floor": 1, "accessible": True},
            {"id": "union_book", "name": "University Bookstore & Merch", "floor": 1, "accessible": True},
            {"id": "union_lounge", "name": "Student Government & Game Zone", "floor": 2, "accessible": True},
            {"id": "union_atm", "name": "Campus Bank & ATMs", "floor": 1, "accessible": True}
        ]
    },
    "b_auditorium": {
        "id": "b_auditorium",
        "name": "Grand Arts & Cultural Auditorium",
        "short_name": "Main Auditorium",
        "category": "Arts / Events",
        "description": "1,200-seat performing arts center for convocation, guest keynotes, and concerts",
        "position": [560, 150],
        "polygon": [[500, 90], [500, 210], [620, 210], [620, 90]],
        "entrance_node": "n_aud_ent",
        "color": "#dc2626",
        "accent": "#f87171",
        "icon": "mic",
        "accessible": True,
        "floors": 2,
        "has_elevator": True,
        "operating_hours": "Event hours & 09:00 - 18:00",
        "rooms": [
            {"id": "aud_main", "name": "Main Concert Hall", "floor": 1, "accessible": True},
            {"id": "aud_gallery", "name": "Balcony & Fine Arts Gallery", "floor": 2, "accessible": True},
            {"id": "aud_green", "name": "Green Rooms & Rehearsal", "floor": 1, "accessible": True}
        ]
    },
    "b_health": {
        "id": "b_health",
        "name": "Student Health & Wellness Clinic",
        "short_name": "Health Center",
        "category": "Health & Emergency",
        "description": "Urgent primary care, pharmacy, counseling center, and 24/7 campus first-aid dispatch",
        "position": [560, 780],
        "polygon": [[500, 720], [500, 840], [620, 840], [620, 720]],
        "entrance_node": "n_health_ent",
        "color": "#e11d48",
        "accent": "#fb7185",
        "icon": "heart-pulse",
        "accessible": True,
        "floors": 2,
        "has_elevator": True,
        "operating_hours": "Urgent Care: 24/7, Pharmacy: 08:00 - 20:00",
        "rooms": [
            {"id": "hlth_triage", "name": "Urgent Care & Triage", "floor": 1, "accessible": True},
            {"id": "hlth_pharm", "name": "Student Pharmacy", "floor": 1, "accessible": True},
            {"id": "hlth_counsel", "name": "Mindfulness & Mental Health", "floor": 2, "accessible": True}
        ]
    },
    "b_sports": {
        "id": "b_sports",
        "name": "Athletics Arena & Recreation Complex",
        "short_name": "Sports Complex",
        "category": "Athletics",
        "description": "Gymnasium, basketball arenas, Olympic swimming pool, indoor track and courts",
        "position": [700, 600],
        "polygon": [[650, 500], [650, 700], [750, 700], [750, 500]],
        "entrance_node": "n_sports_ent",
        "color": "#0d9488",
        "accent": "#2dd4bf",
        "icon": "trophy",
        "accessible": True,
        "floors": 2,
        "has_elevator": True,
        "operating_hours": "06:00 - 23:00",
        "rooms": [
            {"id": "sp_gym", "name": "Cardio & Weight Training Center", "floor": 1, "accessible": True},
            {"id": "sp_bball", "name": "Varsity Basketball Arena", "floor": 1, "accessible": True},
            {"id": "sp_pool", "name": "Aquatics & Olympic Pool", "floor": 1, "accessible": True},
            {"id": "sp_studio", "name": "Yoga & Dance Studio", "floor": 2, "accessible": True}
        ]
    },
    "b_dorms_north": {
        "id": "b_dorms_north",
        "name": "North Residential Village (Dorms A & B)",
        "short_name": "North Dorms",
        "category": "Housing",
        "description": "Undergraduate residence halls, study pods, laundry, courtyard dining",
        "position": [100, 180],
        "polygon": [[60, 100], [60, 260], [140, 260], [140, 100]],
        "entrance_node": "n_dorm_n_ent",
        "color": "#4b5563",
        "accent": "#9ca3af",
        "icon": "bed",
        "accessible": True,
        "floors": 4,
        "has_elevator": True,
        "operating_hours": "Resident Keycard 24/7",
        "rooms": [
            {"id": "dorm_n_lounge", "name": "North Commons Lounge", "floor": 1, "accessible": True},
            {"id": "dorm_n_laundry", "name": "North Village Laundry", "floor": 1, "accessible": True}
        ]
    },
    "b_dorms_south": {
        "id": "b_dorms_south",
        "name": "South Lakeside Residences (Dorms C & D)",
        "short_name": "South Dorms",
        "category": "Housing",
        "description": "Senior student apartments and graduate housing suites overlooking the lake",
        "position": [700, 250],
        "polygon": [[650, 180], [650, 320], [750, 320], [750, 180]],
        "entrance_node": "n_dorm_s_ent",
        "color": "#4b5563",
        "accent": "#9ca3af",
        "icon": "bed",
        "accessible": True,
        "floors": 4,
        "has_elevator": True,
        "operating_hours": "Resident Keycard 24/7",
        "rooms": [
            {"id": "dorm_s_lounge", "name": "South Commons Social Hall", "floor": 1, "accessible": True}
        ]
    },
    "b_transit": {
        "id": "b_transit",
        "name": "Central Campus Transit Hub & Shuttle Terminal",
        "short_name": "Transit Hub",
        "category": "Transportation",
        "description": "City bus connections, campus electric shuttle station, EV charging and e-bike rentals",
        "position": [400, 20],
        "polygon": [[360, 5], [360, 45], [440, 45], [440, 5]],
        "entrance_node": "n_transit_ent",
        "color": "#15803d",
        "accent": "#4ade80",
        "icon": "bus",
        "accessible": True,
        "floors": 1,
        "has_elevator": True,
        "operating_hours": "05:30 - 01:00",
        "rooms": [
            {"id": "tr_bus", "name": "Bus Bays 1-4", "floor": 1, "accessible": True},
            {"id": "tr_bike", "name": "Smart Bike Share Dock", "floor": 1, "accessible": True}
        ]
    }
}

# Outdoor Parks & Landmarks (Visual & Geo reference)
LANDMARKS = [
    {
        "id": "lm_quad",
        "name": "Central Memorial Quad & Great Lawn",
        "category": "Outdoor Landmark",
        "position": [400, 360],
        "polygon": [[340, 280], [340, 440], [460, 440], [460, 280]],
        "color": "#16a34a",
        "description": "Vibrant green open field, campus gatherings, outdoor study, and Wi-Fi zone"
    },
    {
        "id": "lm_fountain",
        "name": "Solar Jubilee Fountain",
        "category": "Landmark",
        "position": [400, 360],
        "radius": 15,
        "color": "#0ea5e9",
        "description": "Prominent central meeting spot and geographic center of campus"
    },
    {
        "id": "lm_botanical",
        "name": "Zen Botanical Garden & Rose Walk",
        "category": "Garden",
        "position": [700, 420],
        "polygon": [[660, 370], [660, 470], [740, 470], [740, 370]],
        "color": "#15803d",
        "description": "Peaceful sanctuary with shaded pagodas, koi pond, and sensory paths"
    },
    {
        "id": "lm_track",
        "name": "East Athletics Field & Running Track",
        "category": "Sports",
        "position": [700, 780],
        "polygon": [[650, 720], [650, 840], [750, 840], [750, 720]],
        "color": "#ea580c",
        "description": "Synthetic 400m track and soccer field"
    },
    {
        "id": "lm_park_north",
        "name": "North Visitor & Disability Parking Lot",
        "category": "Parking",
        "position": [100, 400],
        "polygon": [[60, 340], [60, 460], [140, 460], [140, 340]],
        "color": "#64748b",
        "description": "Includes 12 dedicated ADA wheelchair parking spots and EV fast chargers"
    },
    {
        "id": "lm_park_south",
        "name": "South Student & Staff Parking",
        "category": "Parking",
        "position": [560, 930],
        "polygon": [[500, 880], [500, 980], [620, 980], [620, 880]],
        "color": "#64748b",
        "description": "General commuter lot with bike lockers"
    }
]

# Navigation Nodes (Graph vertices)
# Coordinates in [y, x] (Leaflet CRS.Simple convention)
NODES: Dict[str, Dict[str, Any]] = {
    # Building Entrances
    "n_transit_ent": {"id": "n_transit_ent", "pos": [400, 45], "name": "Transit Hub Main Entrance", "accessible": True},
    "n_admin_ent": {"id": "n_admin_ent", "pos": [400, 205], "name": "Admin Building Entrance", "accessible": True},
    "n_dorm_n_ent": {"id": "n_dorm_n_ent", "pos": [145, 180], "name": "North Dorms Gateway", "accessible": True},
    "n_cs_ent": {"id": "n_cs_ent", "pos": [305, 350], "name": "CS Institute Main Glass Entrance", "accessible": True},
    "n_einstein_ent": {"id": "n_einstein_ent", "pos": [305, 560], "name": "Lecture Halls South Entrance", "accessible": True},
    "n_eng_ent": {"id": "n_eng_ent", "pos": [305, 780], "name": "Engineering Hub Entrance", "accessible": True},
    "n_union_ent": {"id": "n_union_ent", "pos": [400, 495], "name": "Student Union West Entrance", "accessible": True},
    "n_union_east": {"id": "n_union_east", "pos": [400, 625], "name": "Student Union East Entrance", "accessible": True},
    "n_lib_ent": {"id": "n_lib_ent", "pos": [495, 360], "name": "Library Plaza Entrance", "accessible": True},
    "n_aud_ent": {"id": "n_aud_ent", "pos": [495, 150], "name": "Auditorium Main Portico", "accessible": True},
    "n_health_ent": {"id": "n_health_ent", "pos": [495, 780], "name": "Health Center Triage Doors", "accessible": True},
    "n_sports_ent": {"id": "n_sports_ent", "pos": [645, 600], "name": "Sports Complex Front Gate", "accessible": True},
    "n_dorm_s_ent": {"id": "n_dorm_s_ent", "pos": [645, 250], "name": "South Dorms Courtyard", "accessible": True},
    
    # Major Walkway Intersections & Landmarks
    "n_north_gate": {"id": "n_north_gate", "pos": [400, 90], "name": "North Concourse Junction", "accessible": True},
    "n_quad_west": {"id": "n_quad_west", "pos": [400, 260], "name": "Admin-Quad Walkway Junction", "accessible": True},
    "n_quad_center": {"id": "n_quad_center", "pos": [400, 360], "name": "Central Solar Fountain Plaza", "accessible": True},
    "n_quad_east": {"id": "n_quad_east", "pos": [400, 460], "name": "Library-Union Concourse", "accessible": True},
    "n_academic_north": {"id": "n_academic_north", "pos": [240, 260], "name": "North Academic Lane", "accessible": True},
    "n_academic_spine_1": {"id": "n_academic_spine_1", "pos": [240, 450], "name": "Academic Spine - CS & Einstein Junction", "accessible": True},
    "n_academic_spine_2": {"id": "n_academic_spine_2", "pos": [240, 670], "name": "Academic Spine - Einstein & Eng Junction", "accessible": True},
    "n_eng_junction": {"id": "n_eng_junction", "pos": [400, 780], "name": "East Campus Crossway", "accessible": True},
    "n_south_lane_1": {"id": "n_south_lane_1", "pos": [560, 260], "name": "Auditorium-Library Walk", "accessible": True},
    "n_south_lane_2": {"id": "n_south_lane_2", "pos": [560, 460], "name": "Library-Sports Promenade", "accessible": True},
    "n_south_lane_3": {"id": "n_south_lane_3", "pos": [560, 670], "name": "Sports & Health Connector", "accessible": True},
    "n_botanical_junction": {"id": "n_botanical_junction", "pos": [640, 360], "name": "Botanical Garden Entrance", "accessible": True},
    "n_north_park_ent": {"id": "n_north_park_ent", "pos": [145, 400], "name": "North Parking ADA Path", "accessible": True},
    "n_south_park_ent": {"id": "n_south_park_ent", "pos": [560, 875], "name": "South Parking Pedestrian Gate", "accessible": True},

    # Special Accessibility Demonstration Nodes:
    # 1. Monumental Steps between Library Plaza and Central Fountain: Fast for pedestrians, impassable for wheelchairs.
    # 2. ADA Gentle Sloped Ramp with Handrail running parallel: 100% accessible.
    "n_lib_stairs_top": {"id": "n_lib_stairs_top", "pos": [450, 360], "name": "Library Grand Stone Steps (Stairs)", "accessible": False},
    "n_lib_ramp_mid": {"id": "n_lib_ramp_mid", "pos": [445, 385], "name": "Library Accessible Curved Ramp", "accessible": True},
}

# Graph Edges (Walkways connecting nodes)
# edge = {from, to, distance (meters), accessible, surface, stairs: bool, description}
EDGES: List[Dict[str, Any]] = [
    # Transit Hub to North Concourse & Admin
    {"u": "n_transit_ent", "v": "n_north_gate", "weight": 45, "accessible": True, "surface": "Smooth Pavement", "stairs": False},
    {"u": "n_north_gate", "v": "n_admin_ent", "weight": 115, "accessible": True, "surface": "Smooth Pavement", "stairs": False},
    {"u": "n_north_gate", "v": "n_academic_north", "weight": 230, "accessible": True, "surface": "Paved Sidewalk", "stairs": False},
    {"u": "n_academic_north", "v": "n_dorm_n_ent", "weight": 120, "accessible": True, "surface": "Paved Sidewalk", "stairs": False},
    
    # Admin to Quad
    {"u": "n_admin_ent", "v": "n_quad_west", "weight": 55, "accessible": True, "surface": "Wide Pavers", "stairs": False},
    {"u": "n_admin_ent", "v": "n_aud_ent", "weight": 110, "accessible": True, "surface": "Tree-lined Path", "stairs": False},
    
    # Academic Spine (CS, Einstein, Engineering)
    {"u": "n_academic_north", "v": "n_cs_ent", "weight": 110, "accessible": True, "surface": "Smooth Concrete", "stairs": False},
    {"u": "n_north_park_ent", "v": "n_cs_ent", "weight": 165, "accessible": True, "surface": "ADA Ramped Pavement", "stairs": False},
    {"u": "n_cs_ent", "v": "n_academic_spine_1", "weight": 120, "accessible": True, "surface": "Smooth Concrete", "stairs": False},
    {"u": "n_academic_spine_1", "v": "n_einstein_ent", "weight": 130, "accessible": True, "surface": "Smooth Concrete", "stairs": False},
    {"u": "n_einstein_ent", "v": "n_academic_spine_2", "weight": 130, "accessible": True, "surface": "Smooth Concrete", "stairs": False},
    {"u": "n_academic_spine_2", "v": "n_eng_ent", "weight": 130, "accessible": True, "surface": "Smooth Concrete", "stairs": False},
    
    # Academic Connectors to Central Quad
    {"u": "n_cs_ent", "v": "n_quad_west", "weight": 135, "accessible": True, "surface": "Cobblestone Level Walkway", "stairs": False},
    {"u": "n_quad_west", "v": "n_quad_center", "weight": 100, "accessible": True, "surface": "Central Concourse", "stairs": False},
    {"u": "n_academic_spine_1", "v": "n_quad_center", "weight": 185, "accessible": True, "surface": "Diagonal Walkway", "stairs": False},
    {"u": "n_einstein_ent", "v": "n_union_ent", "weight": 115, "accessible": True, "surface": "Plaza Pavement", "stairs": False},
    {"u": "n_academic_spine_2", "v": "n_eng_junction", "weight": 195, "accessible": True, "surface": "Paved Walkway", "stairs": False},
    {"u": "n_eng_ent", "v": "n_eng_junction", "weight": 95, "accessible": True, "surface": "Paved Walkway", "stairs": False},
    
    # Central Quad & Library paths (WITH STAIRS VS RAMP CHOICE)
    {"u": "n_quad_center", "v": "n_quad_east", "weight": 100, "accessible": True, "surface": "Central Concourse", "stairs": False},
    
    # DIRECT STAIR PATH: 45 meters, has steep stairs, NOT accessible
    {"u": "n_quad_center", "v": "n_lib_stairs_top", "weight": 50, "accessible": False, "surface": "Granite Monumental Stairs (32 steps)", "stairs": True, "name": "Central Grand Steps"},
    {"u": "n_lib_stairs_top", "v": "n_lib_ent", "weight": 45, "accessible": False, "surface": "Library Upper Terrace", "stairs": False},
    
    # ACCESSIBLE RAMP BYPASS: 75 meters, fully ADA compliant gentle slope
    {"u": "n_quad_center", "v": "n_lib_ramp_mid", "weight": 52, "accessible": True, "surface": "Gentle ADA Ramp (1:12 slope)", "stairs": False, "name": "Library South Accessible Ramp"},
    {"u": "n_lib_ramp_mid", "v": "n_lib_ent", "weight": 55, "accessible": True, "surface": "Library Upper Terrace", "stairs": False},
    
    # Student Union connections
    {"u": "n_quad_east", "v": "n_union_ent", "weight": 45, "accessible": True, "surface": "Plaza Pavers", "stairs": False},
    {"u": "n_union_ent", "v": "n_union_east", "weight": 130, "accessible": True, "surface": "Indoor Wide Corridor", "stairs": False},
    {"u": "n_union_east", "v": "n_south_lane_2", "weight": 165, "accessible": True, "surface": "Paved Plaza", "stairs": False},
    
    # Library to South & East Areas
    {"u": "n_lib_ent", "v": "n_south_lane_1", "weight": 120, "accessible": True, "surface": "Tree-lined Path", "stairs": False},
    {"u": "n_lib_ent", "v": "n_south_lane_2", "weight": 120, "accessible": True, "surface": "Stone Promenade", "stairs": False},
    {"u": "n_south_lane_1", "v": "n_aud_ent", "weight": 130, "accessible": True, "surface": "Grand Walkway", "stairs": False},
    {"u": "n_south_lane_1", "v": "n_dorm_s_ent", "weight": 90, "accessible": True, "surface": "Lakeside Pavement", "stairs": False},
    
    # Botanical Garden & Dorm South
    {"u": "n_south_lane_2", "v": "n_botanical_junction", "weight": 125, "accessible": True, "surface": "Garden Path", "stairs": False},
    {"u": "n_botanical_junction", "v": "n_dorm_s_ent", "weight": 110, "accessible": True, "surface": "Shaded Path", "stairs": False},
    
    # Health, Sports & Engineering Junction
    {"u": "n_south_lane_2", "v": "n_south_lane_3", "weight": 210, "accessible": True, "surface": "Boulevard", "stairs": False},
    {"u": "n_south_lane_3", "v": "n_sports_ent", "weight": 110, "accessible": True, "surface": "Sports Plaza", "stairs": False},
    {"u": "n_south_lane_3", "v": "n_health_ent", "weight": 130, "accessible": True, "surface": "Smooth Hospital Approach", "stairs": False},
    {"u": "n_health_ent", "v": "n_south_park_ent", "weight": 115, "accessible": True, "surface": "ADA Sidewalk", "stairs": False},
    {"u": "n_health_ent", "v": "n_eng_junction", "weight": 95, "accessible": True, "surface": "East Concourse", "stairs": False},
    {"u": "n_union_east", "v": "n_eng_junction", "weight": 155, "accessible": True, "surface": "East Concourse", "stairs": False},
]

# Real-Time Class Schedules
CLASS_SCHEDULES = [
    {
        "id": "CS101",
        "title": "Introduction to Computer Science & Python",
        "instructor": "Prof. Alan Mitchell",
        "building_id": "b_einstein",
        "building_name": "Albert Einstein Lecture Halls",
        "room": "Auditorium LH-1",
        "room_id": "lh_1",
        "days": ["Monday", "Wednesday", "Friday"],
        "start_time": "09:00",
        "end_time": "10:30",
        "department": "Computer Science",
        "description": "Fundamental programming paradigms, algorithmic thinking, and problem solving."
    },
    {
        "id": "AI301",
        "title": "Deep Learning & Neural Architectures",
        "instructor": "Dr. Elena Rostova",
        "building_id": "b_cs",
        "building_name": "Computer Science & AI Institute",
        "room": "Deep Learning Arena (CS-204)",
        "room_id": "cs_204",
        "days": ["Tuesday", "Thursday"],
        "start_time": "11:00",
        "end_time": "12:30",
        "department": "Computer Science",
        "description": "Transformers, CNNs, generative modeling and reinforcement learning."
    },
    {
        "id": "MATH202",
        "title": "Multivariable Calculus & Linear Algebra",
        "instructor": "Prof. David Thorne",
        "building_id": "b_einstein",
        "building_name": "Albert Einstein Lecture Halls",
        "room": "Lecture Hall LH-2",
        "room_id": "lh_2",
        "days": ["Monday", "Wednesday"],
        "start_time": "10:00",
        "end_time": "11:30",
        "department": "Mathematics",
        "description": "Matrix factorizations, eigen-decomposition, gradient fields."
    },
    {
        "id": "ENG105",
        "title": "Maker Robotics & 3D Prototyping",
        "instructor": "Dr. Marcus Vance",
        "building_id": "b_eng",
        "building_name": "Engineering & Maker Innovation Hub",
        "room": "MakerSpace (1st Floor)",
        "room_id": "eng_maker",
        "days": ["Monday", "Wednesday", "Friday"],
        "start_time": "14:00",
        "end_time": "16:00",
        "department": "Engineering",
        "description": "Hands-on micro-controllers, CAD modeling, and rapid prototyping."
    },
    {
        "id": "ENG302",
        "title": "Senior Capstone Design Studio",
        "instructor": "Prof. Sarah Sterling",
        "building_id": "b_eng",
        "building_name": "Engineering & Maker Innovation Hub",
        "room": "Studio 302",
        "room_id": "eng_302",
        "days": ["Tuesday", "Thursday"],
        "start_time": "13:30",
        "end_time": "15:00",
        "department": "Engineering",
        "description": "Multi-disciplinary team engineering product development."
    },
    {
        "id": "CHEM110",
        "title": "General Chemistry & Lab Techniques",
        "instructor": "Dr. Rebecca Lin",
        "building_id": "b_einstein",
        "building_name": "Albert Einstein Lecture Halls",
        "room": "Chemistry Amphitheatre",
        "room_id": "lh_amph",
        "days": ["Monday", "Wednesday"],
        "start_time": "14:00",
        "end_time": "15:30",
        "department": "Chemistry",
        "description": "Atomic structure, chemical kinetics, stoichiometry."
    }
]

# Campus Events
CAMPUS_EVENTS = [
    {
        "id": "evt_hackathon",
        "title": "Annual 36-Hour Hackathon Kickoff & Showcase",
        "category": "Technology & Innovation",
        "building_id": "b_auditorium",
        "building_name": "Grand Arts Auditorium",
        "room": "Main Concert Hall",
        "room_id": "aud_main",
        "time": "16:00 - 19:30 Today",
        "status": "Starting Soon",
        "description": "Keynotes from tech founders, team formation, and hardware API demos.",
        "badge": "Hot Event"
    },
    {
        "id": "evt_career_fair",
        "title": "Fall STEM Career & Internship Fair",
        "category": "Career & Networking",
        "building_id": "b_student_union",
        "building_name": "Student Union Pavilion",
        "room": "Food Court & Upper Commons",
        "room_id": "din_main",
        "time": "10:00 - 16:30 Today",
        "status": "Happening Now",
        "description": "Over 60 technology, biotech, and engineering firms recruiting on campus.",
        "badge": "Happening Now"
    },
    {
        "id": "evt_robotics_demo",
        "title": "Autonomous Drone & Quadruped Live Demo",
        "category": "Robotics",
        "building_id": "b_cs",
        "building_name": "Computer Science & AI Institute",
        "room": "CS Courtyard / CS-204",
        "room_id": "cs_204",
        "time": "15:00 - 16:15 Today",
        "status": "Upcoming",
        "description": "Watch autonomous navigation algorithms tested on quadruped robots.",
        "badge": "Demo"
    },
    {
        "id": "evt_wellness_yoga",
        "title": "Sunset Mindfulness & Flow Yoga",
        "category": "Wellness",
        "building_id": "b_sports",
        "building_name": "Athletics Arena",
        "room": "Studio B (2nd Floor)",
        "room_id": "sp_studio",
        "time": "17:30 - 18:30 Today",
        "status": "Upcoming",
        "description": "Free beginner-friendly yoga session for students and staff. Mats provided.",
        "badge": "Wellness"
    }
]

# Points of Interest (POIs) & Amenities (Restrooms, Cafes, ATMs, First Aid, Water Stations)
AMENITIES = [
    {"id": "amen_cafe_1", "type": "cafe", "name": "The Daily Grind Espresso", "building_id": "b_student_union", "node": "n_union_ent", "pos": [400, 520], "accessible": True},
    {"id": "amen_cafe_2", "type": "cafe", "name": "Library Coffee Pod", "building_id": "b_library", "node": "n_lib_ent", "pos": [540, 360], "accessible": True},
    {"id": "amen_atm_1", "type": "atm", "name": "Campus Credit Union ATM", "building_id": "b_student_union", "node": "n_union_ent", "pos": [410, 540], "accessible": True},
    {"id": "amen_atm_2", "type": "atm", "name": "Transit Hub 24/7 ATM", "building_id": "b_transit", "node": "n_transit_ent", "pos": [400, 30], "accessible": True},
    {"id": "amen_wc_1", "type": "restroom", "name": "All-Gender Accessible Restrooms", "building_id": "b_student_union", "node": "n_union_ent", "pos": [400, 570], "accessible": True},
    {"id": "amen_wc_2", "type": "restroom", "name": "Central Library ADA Restrooms", "building_id": "b_library", "node": "n_lib_ent", "pos": [570, 360], "accessible": True},
    {"id": "amen_wc_3", "type": "restroom", "name": "CS Building Wheelchair Restrooms", "building_id": "b_cs", "node": "n_cs_ent", "pos": [230, 360], "accessible": True},
    {"id": "amen_aid_1", "type": "first_aid", "name": "Urgent Care First Aid & AED", "building_id": "b_health", "node": "n_health_ent", "pos": [560, 770], "accessible": True},
    {"id": "amen_bike_1", "type": "bike", "name": "Electric Bike Rental Dock", "building_id": "b_transit", "node": "n_transit_ent", "pos": [415, 35], "accessible": True},
]
