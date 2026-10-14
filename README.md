# 🏛️ ApexNav - AI Campus Navigation Assistant

An intelligent, interactive Campus Navigation Assistant designed for university students, faculty, and visitors. ApexNav pairs graph-based shortest path routing with an AI conversational assistant, real-time schedule lookups, and dedicated wheelchair accessibility navigation.

---

## ✨ Key Features

1. **Interactive 2D Campus Map**:
   - High-fidelity campus vector map built with Leaflet.js (`CRS.Simple`).
   - Detailed footprints for Academic Blocks, Central Library, Student Union, Residence Halls, Labs, and Sports Arenas.
   - Interactive POIs: Restrooms, Cafeterias, ATMs, First Aid Stations, and Bike Share Docks.

2. **Smart Shortest Path Navigation (A* & Dijkstra)**:
   - High-precision pathfinding between any campus buildings, rooms, or user location.
   - Computes distance in meters, estimated walking time in minutes, burned calories, and step count.
   - Step-by-step turn-by-turn navigation instructions with directional cues (e.g., *"Bear slight right past Solar Fountain Plaza"*).

3. **Dedicated Wheelchair Accessibility Mode**:
   - Barrier-free routing that completely avoids outdoor monumental staircases.
   - Automatically prioritizes ADA-certified gentle ramps, wide concourses, and elevators.
   - Visual badges highlighting ramp approaches vs stair warnings.

4. **AI Conversational & Voice Assistant (NavBot)**:
   - Natural Language Understanding (NLU) for routing queries (*"How do I get to the Library from North Dorms?"*), room queries (*"Where is CS101?"*), and amenity searches (*"Where can I get coffee?"*).
   - Web Speech API integration:
     - **Speech-to-Text**: Hands-free voice input via microphone.
     - **Text-to-Speech**: Spoken navigation and answers.
   - Interactive chat action cards that link directly to map actions.
   - Optional external LLM support (Google Gemini) via API key.

5. **Real-Time Class Schedule & Event Locator**:
   - Course timetable database (CS101, AI301, MATH202, etc.) with building, room, instructor, and time slots.
   - Campus event calendar (Hackathons, Career Fairs, Robotics Demos, Yoga).
   - 1-click **"Guide Me There"** button to start instant navigation to any class or event.

6. **Interactive Walk Simulation**:
   - Watch an animated walker avatar travel along the selected route on the map in real-time, stepping through turn-by-turn guidance.

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.10+ (Tested on Python 3.14)
- Flask (already installed or `pip install -r requirements.txt`)

### 2. Run the Application
```bash
python app.py
```

### 3. Open in Browser
Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser (Chrome or Edge recommended for full Web Speech API voice support).

---

## 📁 Project Architecture

```
Campus Navigation Assistant/
├── app.py                 # Flask web server & REST endpoints
├── campus_data.py         # Campus graph nodes, edges, buildings, amenities, schedules
├── pathfinding.py         # A* / Dijkstra pathfinding & turn-by-turn generator
├── ai_assistant.py        # Conversational NLU engine & intent processor
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css      # Glassmorphism theme, animations & badges
│   └── js/
│       ├── map.js         # Leaflet map vector rendering & route layer
│       ├── navigation.js  # Route planner, metrics & voice guidance
│       ├── chat.js        # AI chat drawer & speech recognition/synthesis
│       ├── schedule.js    # Class timetable & event manager
│       └── app.js         # Main UI orchestration
└── templates/
    └── index.html         # Responsive dashboard UI
```

---

## 💬 Sample Voice / AI Assistant Queries

- *"Where is the CS101 lecture right now?"*
- *"How do I get from North Dorms to Alan Turing Library?"*
- *"I need a wheelchair-friendly route to the Auditorium."*
- *"Where can I get coffee?"*
- *"What events are happening today?"*
- *"Where is the urgent care clinic?"*
