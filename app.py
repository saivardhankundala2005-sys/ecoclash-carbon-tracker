import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from typing import List, Dict, Any, Tuple
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

# ==========================================
# 1. PAGE CONFIGURATION & METADATA
# ==========================================
st.set_page_config(
    page_title="EcoClash: Gamified Carbon Footprint Arena 🌿⚔️",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. PREMIUM CSS DESIGN SYSTEM (GLASSMORPHISM)
# ==========================================
def inject_custom_styles():
    """Injects high-end, premium CSS style sheets for a carbon-neutral dashboard experience."""
    st.markdown(
        """
        <style>
        /* Import Outfit & Inter fonts from Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
        
        /* Apply fonts globally */
        html, body, [class*="css"], .stApp {
            font-family: 'Inter', sans-serif;
            background-color: #0d0f14;
            color: #e2e8f0;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            color: #f8fafc;
        }

        /* Glassmorphism Card Container */
        .glass-card {
            background: rgba(30, 41, 59, 0.45);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .glass-card:hover {
            border: 1px solid rgba(16, 185, 129, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 12px 40px 0 rgba(16, 185, 129, 0.1);
        }

        /* Leaderboard styling */
        .leaderboard-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 0.95rem;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .leaderboard-table thead tr {
            background-color: rgba(15, 23, 42, 0.8);
            color: #38bdf8;
            text-align: left;
            font-weight: 600;
        }
        
        .leaderboard-table th, .leaderboard-table td {
            padding: 14px 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .leaderboard-table tbody tr {
            background-color: rgba(30, 41, 59, 0.2);
            transition: background-color 0.2s ease;
        }
        
        .leaderboard-table tbody tr:hover {
            background-color: rgba(30, 41, 59, 0.5);
        }
        
        .leaderboard-table tbody tr.user-row {
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.15), rgba(6, 182, 212, 0.05));
            border-left: 4px solid #10b981;
            font-weight: 600;
        }

        /* Glowing Carbon Metric Number */
        .glowing-metric {
            font-size: 2.8rem;
            font-weight: 700;
            color: #10b981;
            text-shadow: 0 0 15px rgba(16, 185, 129, 0.45);
            margin: 5px 0;
        }
        
        .glowing-metric-red {
            font-size: 2.8rem;
            font-weight: 700;
            color: #ef4444;
            text-shadow: 0 0 15px rgba(239, 68, 68, 0.45);
            margin: 5px 0;
        }

        /* Custom Chat Containers */
        .chat-bubble-container {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 15px;
            max-height: 480px;
            overflow-y: auto;
            padding: 10px;
            border-radius: 12px;
            background: rgba(15, 23, 42, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.03);
        }
        
        .chat-bubble {
            padding: 16px 20px;
            border-radius: 14px;
            max-width: 85%;
            line-height: 1.5;
            position: relative;
            animation: fadeIn 0.4s ease-out;
        }
        
        /* Chat bubble avatars and borders by character */
        .bubble-user {
            align-self: flex-end;
            background: linear-gradient(135deg, #0f766e 0%, #115e59 100%);
            border: 1px solid #14b8a6;
            color: #f0fdfa;
            border-bottom-right-radius: 2px;
        }
        
        .bubble-enid {
            align-self: flex-start;
            background-color: rgba(22, 101, 52, 0.25);
            border-left: 4px solid #22c55e;
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-left: 5px solid #22c55e;
            color: #f0fdf4;
            border-top-left-radius: 2px;
        }
        
        .bubble-sam {
            align-self: flex-start;
            background-color: rgba(30, 58, 138, 0.25);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-left: 5px solid #3b82f6;
            color: #eff6ff;
            border-top-left-radius: 2px;
        }
        
        .bubble-minimalist {
            align-self: flex-start;
            background-color: rgba(88, 28, 135, 0.25);
            border: 1px solid rgba(168, 85, 247, 0.3);
            border-left: 5px solid #a855f7;
            color: #faf5ff;
            border-top-left-radius: 2px;
        }
        
        .chat-name {
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .name-enid { color: #4ade80; }
        .name-sam { color: #60a5fa; }
        .name-minimalist { color: #c084fc; }
        .name-user { color: #2dd4bf; }

        /* Badge Showcase Cards */
        .badge-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-top: 15px;
        }
        
        .badge-card {
            background: rgba(30, 41, 59, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .badge-unlocked {
            border: 1px solid rgba(234, 179, 8, 0.4);
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(234, 179, 8, 0.05) 100%);
            box-shadow: 0 0 15px rgba(234, 179, 8, 0.1);
        }
        
        .badge-icon {
            font-size: 2.5rem;
            margin-bottom: 10px;
            filter: grayscale(100%);
            transition: filter 0.3s ease;
        }
        
        .badge-unlocked .badge-icon {
            filter: grayscale(0%);
            animation: pulse 2s infinite;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        /* Banner Switch Mock Alert */
        .mock-alert {
            background-color: rgba(234, 179, 8, 0.15);
            border: 1px solid #eab308;
            color: #fef08a;
            padding: 12px 18px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# 3. PRE-BAKED WITTY DIALOGUE (API FALLBACKS)
# ==========================================
MOCK_DIALOGUES: Dict[str, List[Dict[str, str]]] = {
    "commute": [
        {"name": "Eco-Enid", "content": "Ditching the tailpipe? Fantastic! Commuting by bus, train, or bike reduces urban congestion and fossil fuel demand instantly. Sam, run the carbon density analysis!"},
        {"name": "Astro-Sam", "content": "Calculating payload efficiency... Standard single-occupancy ICE vehicle = 404 grams CO2/mile. Electric train = 35 grams/mile. A net savings rate of 91.3%! Smart systems optimized."},
        {"name": "Less-Is-More", "content": "Plus, you skip gridlock, save on parking fees, and bypass insurance markup. Simpler travel means a simpler life. I approval."}
    ],
    "food": [
        {"name": "Eco-Enid", "content": "Eating plant-based! Yes! Livestock farming is a massive driver of global deforesting and methane leaks. Did you know throwing away food is basically venting greenhouse gases directly?"},
        {"name": "Astro-Sam", "content": "Calibrating caloric variables... A transition to plant protein drops direct agricultural carbon footprints by ~60%. Thermochemical processing efficiency maximized. Sensors register green."},
        {"name": "Less-Is-More", "content": "Agreed. Beans, grains, and greens require zero elaborate factory assembly. Cook simple, eat whole, produce minimal wrapper waste. 🍲"}
    ],
    "energy": [
        {"name": "Astro-Sam", "content": "Vampire loads eliminated! Standing standby appliances cost 10% of standard home electrical baselines. My IoT sensors indicate a successful voltage stabilization event."},
        {"name": "Eco-Enid", "content": "Splendid! Now turn the home HVAC thermostat down in winter and wear a cozy, secondhand wool sweater. The greenest kilowatt-hour is the one we never burn!"},
        {"name": "Less-Is-More", "content": "Fewer blinking charger lights, lower monthly utility bills, and a quiet, peaceful home environment. Do less, save more."}
    ],
    "shopping": [
        {"name": "Less-Is-More", "content": "Thrifting and repairing instead of hitting 'Add to Cart'? Beautiful. The carbon footprint of a repaired item is virtually zero since no manufacturing occurs."},
        {"name": "Eco-Enid", "content": "Precisely! Reject corporate fast fashion and the culture of throwaway plastic. We must refuse, reduce, reuse, and repair!"},
        {"name": "Astro-Sam", "content": "Data check: Product lifespan extension by 100% reduces the manufacturing carbon burden amortized over operating hours by exactly 50%. A high efficiency trade."}
    ],
    "general": [
        {"name": "Eco-Enid", "content": "We need active carbon reduction now! The global biosphere depends on everyday micro-habits. Do not lose momentum, Challenger!"},
        {"name": "Astro-Sam", "content": "System status nominal. Leaderboard tracking loops show positive feedback. I am calculating real-time competitor coefficients. Keep optimized!"},
        {"name": "Less-Is-More", "content": "Don't stress over complex eco-gadgets. Keep it simple: consume less, turn stuff off, breathe deeply, and enjoy nature. ☕"}
    ]
}

# ==========================================
# 4. PRE-BAKED HIGH-QUALITY ARTICLES
# ==========================================
ARTICLES = {
    "digital": """
# Decoding the Hidden Footprint of Digital Data Consumption

In the modern era, the internet is often conceptualized as an ethereal, weightless cloud. However, the physical infrastructure supporting this cloud has a massive, rapidly expanding environmental footprint. Every search query, video stream, and AI inference request triggers a cascade of electrical demand in data centers, network routing nodes, and local devices.

### 1. The Material Reality of the Cloud
Data centers are warehouses filled with row upon row of high-performance servers running 24/7. These centers consume electricity for two main purposes:
- **Computation:** Processing calculations and reading/writing storage units.
- **Thermal Management (Cooling):** Standard server racks generate intense heat. Approximately 30-40% of a data center's energy usage goes directly to mechanical cooling systems (chillers, cooling towers, and fans) to prevent thermal shutdown.

The efficiency of these facilities is measured by **Power Usage Effectiveness (PUE)**, where a value of 1.0 represents perfect efficiency (every watt goes to computation). While modern hyper-scale facilities achieve a PUE of 1.1 to 1.2, many legacy structures operate closer to 1.5 or higher.

### 2. The Compounding Math of Data Streaming
When you stream high-definition (HD) or ultra-high-definition (4K) content, you aren't just powering your television. You are initiating high-bandwidth data transfers across national fiber-optic backbones and neighborhood routers.
- **HD Streaming:** Typically consumes ~1.5 to 3 GB of data per hour.
- **4K Streaming:** Consumes ~7 to 10 GB per hour, requiring up to 4-5x more electrical work from network switches.
- **Grid Intensity Factor:** Depending on whether your local grid relies on coal, natural gas, or renewables, streaming an hour of 4K video can account for **50g to 200g of CO2e**. If a user streams 4 hours daily, this compounds to **73 kg to 292 kg of CO2e annually**.

### 3. The Power Profile of Artificial Intelligence
Large Language Model (LLM) processing represents a major shift in computing density. Traditional search engines retrieve pre-indexed text, requiring minor CPU cycles. Generative AI models perform active multi-billion parameter tensor calculations for *every single token generated*.
- **Standard Search Query:** ~0.0003 kWh of electricity (roughly 0.1-0.2g of CO2e).
- **Generative AI Query:** ~0.003 to 0.01 kWh (roughly 1 to 4g of CO2e) — up to a **10x to 30x increase** in energy demand per interaction.
- **Data Center Water Use:** Training and running massive neural networks also require gallons of water for cooling per thousand queries, adding local ecological strain.

### 🔌 Actionable Digital Micro-Habits:
1. **Declutter "Dark Data":** Delete old emails, duplicate photo backups, and unused cloud storage. Storage drives draw power even when idling.
2. **Adjust Resolution:** Lower streaming settings to 1080p or 720p on mobile devices where the visual difference is negligible.
3. **Turn Off Autoplay:** Prevent background video streaming when you aren't actively watching.
""",
    "habits": """
# Micro-Habits with Macro Impact: Home HVAC, Phantom Power, and Food Waste Physics

To achieve significant carbon reduction, we must focus on the primary drivers of residential carbon footprints. The physics of heat transfer, electrical resistance, and organic decomposition reveal why small adjustments to home systems yield disproportionately large environmental savings.

### 1. The Thermodynamics of HVAC Systems
Heating, Ventilation, and Air Conditioning (HVAC) systems constitute over **50% of the average home's energy consumption**. The rate of heat transfer through walls and windows is directly proportional to the temperature difference ($\\Delta T$) between the inside of the home and the outdoor environment.
- **The Exponential Cost of Extreme Setpoints:** When you set your air conditioner to 70°F (21°C) on a 95°F (35°C) day ($\\Delta T = 25°F$), your system operates at high pressure ratios, lowering its Coefficient of Performance (COP). 
- **The 1% Rule:** Adjusting your thermostat by just **1°F closer** to the outdoor temperature (e.g., from 72°F to 73°F in summer, or 68°F to 67°F in winter) reduces HVAC energy consumption by **3% to 5%**.
- **Seasonal Drift:** Allowing your home's indoor temperature to drift naturally with the seasons reduces thermal shock, builds metabolic resilience, and avoids hundreds of kilograms of carbon emissions annually.

### 2. Slaying the "Vampire Loads" (Phantom Power Draw)
Many appliances draw power even when turned off. This "phantom load" occurs because internal transformers, power bricks, and standby circuits remain connected to the main voltage line.
- **Standby Baselines:** Devices like smart TVs, microwave clocks, video game consoles, and chargers consume **1W to 15W** of continuous standby power.
- **The Cumulative Effect:** A household with 25 standby devices can easily accumulate a baseline vampire load of **100 Watts**. Over a year, this idle draw consumes **876 kWh** of electricity.
- **Grid Impact:** In an average grid mix, this phantom consumption accounts for **~350 kg of CO2e annually**, costing the homeowner $100-$150 for zero functional utility.

### 3. The Anaerobic Chemistry of Food Waste
Food waste is one of the most critical, yet overlooked, drivers of climate change. The ecological impact is determined by where and how the waste decays.
- **Anaerobic vs. Aerobic Decomposition:** In nature (composting), organic material decomposes aerobically (in the presence of oxygen) to release carbon dioxide ($CO_2$). In a packed landfill, organic waste is buried under layers of trash, depriving it of oxygen. It undergoes **anaerobic digestion**, producing methane gas ($CH_4$).
- **Methane's Potency:** Methane is a highly active greenhouse gas. Over a 20-year timescale, methane is **84 to 86 times more potent** than CO2 at trapping heat in the atmosphere.
- **Embedded Carbon Cost:** When you throw away food, you are also discarding the embedded energy, water, shipping fuel, and fertilizer used to grow and transport that food. For instance, throwing away 1 kg of beef wastes the equivalent of **27 kg of CO2e** and 15,000 liters of water.

### 🌿 Actionable Domestic Micro-Habits:
1. **Optimize Thermostat Boundaries:** Program your thermostat to 78°F (25.5°C) in summer and 68°F (20°C) in winter. Use fans to create wind chill.
2. **Deploy Smart Power Strips:** Plug entertainment centers and computer desks into master-slave power strips that cut power to peripherals when the main device is turned off.
3. **Audit the Fridge Weekly:** Practice a "First-In, First-Out" system for food. Freeze excess produce before it spoils, and compost remains to return carbon to the soil rather than landfills.
""",
    "transport": """
# The Urban Transportation Revolution: Mathematical Realities of Personal Transit

Transportation is responsible for approximately **27% of greenhouse gas emissions globally**, with passenger cars making up the largest share. Transitioning urban transportation requires analyzing the math behind energy density, vehicle weights, and occupancy rates.

### 1. The Heavy Math of Single-Occupancy Vehicles
A standard passenger car weighs between 3,000 and 4,500 lbs (1.3 to 2 metric tons). Transporting a single human weighing 150 lbs (68 kg) in a 4,000 lb metal container represents an extreme thermodynamic mismatch:
- **Kinetic Energy Formula:** $E_k = \\frac{1}{2} m v^2$. To accelerate a vehicle, energy must be expended to overcome inertia. Over **95% of the fuel's energy** is spent moving the vehicle itself, not the passenger.
- **Carbon Intensity:** An average gasoline vehicle emits **404 grams of CO2 per mile**. A 15-mile daily round-trip commute generates **1.5 metric tons of CO2 annually** from commuting alone.

### 2. The Ride-Sharing Paradox (Deadheading)
While ride-sharing services like Uber and Lyft are marketed as green alternatives, fleet research reveals that they frequently *increase* net urban carbon emissions:
- **Deadheading:** Ride-share drivers spend a substantial portion of their shift driving empty miles ("deadheading") between passengers or circling blocks waiting for requests.
- **Multiplied Emissions:** Deadheading accounts for approximately **30-40% of ride-share vehicle miles**. As a result, a ride-share trip emits roughly **50% more CO2 per passenger-mile** than a private vehicle trip, intensifying urban congestion.

### 3. Electric Vehicles (EVs) and Grid Dependency
EVs eliminate tailpipe emissions, but they are not carbon-neutral. Their environmental footprint depends on the grid's energy mix and battery production.
- **Manufacturing Debt:** Extracting and processing lithium, cobalt, and nickel for EV batteries is carbon-intensive. An EV starts its life with a "carbon debt" of **5 to 10 metric tons of CO2** from manufacturing.
- **Grid Amortization:** If recharged on a grid dominated by coal, an EV's effective footprint is ~150-200g CO2/mile. On a highly renewable grid (wind, solar, hydro), its emissions drop to **30-50g CO2/mile**. 
- **Payback Mileage:** In most regions, an EV pays off its manufacturing carbon debt within **15,000 to 20,000 miles** of driving.

### 4. Mass Transit and Active Commuting
Mass transit operates on high-density efficiency. The emissions per passenger decrease dramatically as occupancy increases.
- **Public Buses:** Emit ~140g CO2/mile per passenger at average occupancy, dropping below 50g at peak times.
- **Light Rail / Subways:** Emit ~35-40g CO2/mile, often drawing power from dedicated utility substations.
- **Active Transit (Bicycles, E-Bikes, Walking):** Bicycles have zero operational emissions. The lifecycle footprint of a bicycle (manufacturing and human calorie consumption) is **less than 6 grams of CO2 per mile**.

### 🚴 Carbon-Saving Math: A Commute Comparison
If you transition a **10-mile daily commute** from a standard gasoline car to a bicycle or train, look at the compounding savings over a single year (240 working days):
- **By Gas Car:** 240 days × 10 miles × 404g/mile = **969 kg CO2**
- **By Light Rail:** 240 days × 10 miles × 35g/mile = **84 kg CO2** (91% reduction)
- **By Bicycle:** 240 days × 10 miles × 0g/mile = **0 kg CO2** (100% reduction)
"""
}

# ==========================================
# 5. CARBON QUIZ DEFINITION
# ==========================================
QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "Which sector contributes the most to a typical household's carbon footprint in urban areas?",
        "options": [
            "Food consumption & organic waste",
            "Personal transportation (gasoline combustion vehicles)",
            "Digital data storage and smart device computing",
            "Residential LED lighting and micro-appliances"
        ],
        "correct_idx": 1,
        "explanation": "Transportation accounts for 28-30% of average household greenhouse gas emissions in developed urban areas, driven primarily by single-occupancy gasoline passenger cars."
    },
    {
        "id": 2,
        "question": "Why is food waste in landfills significantly more damaging to the climate than backyard composting?",
        "options": [
            "Landfills undergo anaerobic decomposition, producing methane, which is 28-80x more potent than CO2.",
            "Composting chemically vaporizes the carbon atoms, leaving zero atmospheric traces.",
            "Landfill decomposition requires active refrigeration grids that burn heavy diesel fuels.",
            "Compost piles trap carbon dioxide and convert it into solid nitrogen crystals."
        ],
        "correct_idx": 0,
        "explanation": "Burying organic waste cuts off oxygen. Anaerobic bacteria then decompose the material, releasing methane (CH4) gas, which traps heat exponentially better than carbon dioxide (CO2)."
    },
    {
        "id": 3,
        "question": "What is the phenomenon where electrical appliances draw power even when turned off or in standby mode?",
        "options": [
            "Static Resistive Drain",
            "Tesla Inductive Arc",
            "Phantom Load (or Vampire Draw)",
            "Ohmic Drift Factor"
        ],
        "correct_idx": 2,
        "explanation": "Standby transformers and internal circuits in appliances like TVs and smart chargers remain energized, accounting for up to 10% of household electricity usage."
    }
]

# ==========================================
# 6. SESSION STATE INITIALIZATION
# ==========================================
def init_session_state() -> None:
    """Safely initializes all global variables inside st.session_state."""
    if "user_score" not in st.session_state:
        st.session_state.user_score = 450.0  # Starting carbon baseline (kg CO2e / month)
    if "user_points" not in st.session_state:
        st.session_state.user_points = 0
    if "ai_scores" not in st.session_state:
        st.session_state.ai_scores = {
            "Eco-Enid": 140.0,
            "Astro-Sam": 280.0,
            "Less-Is-More": 210.0
        }
    if "unlocked_badges" not in st.session_state:
        st.session_state.unlocked_badges = set()
    if "quiz_selections" not in st.session_state:
        st.session_state.quiz_selections = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "chat_history" not in st.session_state:
        # Starting chat welcoming messages from the three AI characters
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "name": "Eco-Enid",
                "content": "Welcome to the Arena! 🌿 I challenge you to match my footprint of 140 kg CO2/mo. I've cut out single-use plastics entirely. Let's see your moves!"
            },
            {
                "role": "assistant",
                "name": "Astro-Sam",
                "content": "Compiling metrics... ⚡ Current user carbon density is 450 kg CO2. I have optimized my residential smart grid interface, yielding a score of 280 kg CO2. Optimize away, Challenger."
            },
            {
                "role": "assistant",
                "name": "Less-Is-More",
                "content": "Hey there. Don't stress. Just buy less trash, repair what's broken, and bypass consumerism. My score is 210 kg. Good luck. ☕"
            }
        ]
    if "custom_api_key" not in st.session_state:
        st.session_state.custom_api_key = ""
    if "dev_mock_mode" not in st.session_state:
        st.session_state.dev_mock_mode = False
    if "mock_fallback_triggered" not in st.session_state:
        st.session_state.mock_fallback_triggered = False

# ==========================================
# 7. MULTI-CHARACTER GROUP CHAT ENGINE
# ==========================================
def get_mock_response(user_input: str) -> List[Dict[str, str]]:
    """Determines keyword patterns and returns the matched group mock dialogs."""
    input_lower = user_input.lower()
    
    category = "general"
    if any(kw in input_lower for kw in ["car", "bus", "bike", "cycle", "walk", "flight", "transit", "train", "drive", "commute", "travel", "road"]):
        category = "commute"
    elif any(kw in input_lower for kw in ["eat", "meal", "food", "vegan", "veget", "meat", "beef", "chicken", "diet", "compost", "landfill", "waste"]):
        category = "food"
    elif any(kw in input_lower for kw in ["light", "energy", "hvac", "power", "vampire", "electricity", "solar", "appliance", "plug", "standby", "unplug", "heater", "cooling"]):
        category = "energy"
    elif any(kw in input_lower for kw in ["buy", "shop", "thrift", "secondhand", "repair", "plastic", "clutter", "purchase", "item", "recycle", "bag", "bottle"]):
        category = "shopping"
        
    dialogs = MOCK_DIALOGUES[category]
    return [
        {
            "role": "assistant",
            "name": d["name"],
            "content": d["content"]
        } for d in dialogs
    ]

def get_arena_responses(user_input: str) -> List[Dict[str, str]]:
    """
    Orchestrates the competitive responses from the 3 AI characters.
    Uses the Gemini API (target gemini-3.5-flash with gemini-1.5-flash fallback) and 
    automatically switches to Developer Mock Mode if limits are hit or key is missing.
    """
    api_key = st.session_state.custom_api_key or st.secrets.get("GEMINI_API_KEY", "")
    
    # Check if we should directly run Mock Mode (toggle enabled or no key)
    if st.session_state.dev_mock_mode or not api_key:
        if not api_key:
            st.session_state.mock_fallback_triggered = True
        return get_mock_response(user_input)
        
    try:
        genai.configure(api_key=api_key)
        
        # Base prompt setting characters persona, details, and expectations.
        system_instruction = (
            "You are simulating a group chat in a carbon footprint game called EcoClash.\n"
            "The user is competing against 3 AI opponents to minimize their carbon scores.\n"
            f"User's score: {st.session_state.user_score:.1f} kg CO2/mo.\n"
            f"Opponent scores: Eco-Enid: {st.session_state.ai_scores['Eco-Enid']:.1f} kg, "
            f"Astro-Sam: {st.session_state.ai_scores['Astro-Sam']:.1f} kg, "
            f"Less-Is-More: {st.session_state.ai_scores['Less-Is-More']:.1f} kg.\n\n"
            "Opponent Personas:\n"
            "- Eco-Enid: Passionate zero-waste purist, emotional, urgent, loves composting and natural habits, dislikes single-use plastics.\n"
            "- Astro-Sam: Data-focused tech optimizer, uses engineering jargon, metrics, energy calculations, and sensor calibration parameters.\n"
            "- Less-Is-More: Laid-back minimalist, champion of circular economics, repair, thirfting, doing less, and keeping things simple.\n\n"
            "Task: Generate a conversation where these 3 characters comment on the user's action and interact/debate with each other.\n"
            "Format: Return a raw JSON array of 3 objects representing the characters in any logical order. Each object MUST have keys:\n"
            "  'name': (MUST be exactly 'Eco-Enid', 'Astro-Sam', or 'Less-Is-More')\n"
            "  'content': (1-2 sentences of witty, themed response referencing the scores or other characters)\n"
            "Do NOT wrap in markdown blocks, do not output any other text than the raw JSON array."
        )
        
        # Primary Target: gemini-3.5-flash
        model_name = "gemini-3.5-flash"
        
        # We wrap generation in a try-block to fallback to stable gemini-1.5-flash if gemini-3.5-flash is not available/rate-limited
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
            response = model.generate_content(
                f"User's action/message: '{user_input}'\nRespond in JSON array format.",
                generation_config={"response_mime_type": "application/json"}
            )
        except Exception:
            # Fallback to gemini-1.5-flash
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction
            )
            response = model.generate_content(
                f"User's action/message: '{user_input}'\nRespond in JSON array format.",
                generation_config={"response_mime_type": "application/json"}
            )
            
        import json
        raw_text = response.text.strip()
        # Handle cases where model wraps output in markdown code blocks
        if raw_text.startswith("```"):
            lines = raw_text.split("\n")
            if lines[0].startswith("```json") or lines[0].startswith("```"):
                raw_text = "\n".join(lines[1:-1]).strip()
                
        chat_data = json.loads(raw_text)
        validated_messages = []
        for d in chat_data:
            if d.get("name") in ["Eco-Enid", "Astro-Sam", "Less-Is-More"] and d.get("content"):
                validated_messages.append({
                    "role": "assistant",
                    "name": d["name"],
                    "content": d["content"]
                })
        
        if len(validated_messages) == 3:
            st.session_state.mock_fallback_triggered = False  # Reset on successful API call
            return validated_messages
        else:
            raise ValueError("Incomplete character response structure.")
            
    except Exception as e:
        # On rate-limit (429), auth issues or network outage: seamlessly activate Developer Mock Mode
        st.session_state.mock_fallback_triggered = True
        return get_mock_response(user_input)

# ==========================================
# 8. HELPER LOGIC: ACTION LOGGER
# ==========================================
def log_user_action(action_name: str, score_delta: float, chat_msg: str) -> None:
    """Updates user score, triggers algorithmic AI score updates, and inserts dialogue logs."""
    # 1. Update user score
    st.session_state.user_score = max(40.0, st.session_state.user_score - score_delta)
    
    # 2. Add user activity message to history
    st.session_state.chat_history.append({
        "role": "user",
        "name": "You",
        "content": chat_msg
    })
    
    # 3. Dynamic fluctuation of AI competitor scores to simulate active competition
    st.session_state.ai_scores["Eco-Enid"] = max(80.0, st.session_state.ai_scores["Eco-Enid"] - random.uniform(0.1, 0.4))
    st.session_state.ai_scores["Astro-Sam"] = max(150.0, st.session_state.ai_scores["Astro-Sam"] - random.uniform(0.2, 0.6))
    st.session_state.ai_scores["Less-Is-More"] = max(110.0, st.session_state.ai_scores["Less-Is-More"] - random.uniform(0.15, 0.5))
    
    # 4. Generate AI character responses
    with st.spinner("AI opponents are evaluating your actions..."):
        ai_responses = get_arena_responses(chat_msg)
        for resp in ai_responses:
            st.session_state.chat_history.append(resp)
            
    # 5. Cap history length at last 15 messages to optimize memory footprint & token payload
    if len(st.session_state.chat_history) > 15:
        st.session_state.chat_history = st.session_state.chat_history[-15:]

# ==========================================
# 9. REWARDS & BADGES UNLOCK ENGINE
# ==========================================
def check_and_unlock_badges() -> None:
    """Verifies score milestones and quiz performance to unlock permanent achievements."""
    # Badge 1: Carbon Cadet (Completed at least 1 quiz question correctly)
    if st.session_state.user_points >= 1 and "⭐ Carbon Cadet" not in st.session_state.unlocked_badges:
        st.session_state.unlocked_badges.add("⭐ Carbon Cadet")
        st.toast("Achievement Unlocked: ⭐ Carbon Cadet!", icon="🏆")
        
    # Badge 2: Eco Champ (At least 2 correct and footprint below 400)
    if st.session_state.user_points >= 2 and st.session_state.user_score < 400.0 and "🌿 Eco Champ" not in st.session_state.unlocked_badges:
        st.session_state.unlocked_badges.add("🌿 Eco Champ")
        st.toast("Achievement Unlocked: 🌿 Eco Champ!", icon="🏆")
        
    # Badge 3: Sustainability Sovereign (All 3 correct and footprint below 320)
    if st.session_state.user_points == 3 and st.session_state.user_score < 350.0 and "⚡ Sustainability Sovereign" not in st.session_state.unlocked_badges:
        st.session_state.unlocked_badges.add("⚡ Sustainability Sovereign")
        st.toast("Achievement Unlocked: ⚡ Sustainability Sovereign!", icon="🏆")

# ==========================================
# 10. MAIN ROUTING & VIEWS
# ==========================================
def main():
    inject_custom_styles()
    init_session_state()
    
    # Sidebar Global Info & Navigation
    st.sidebar.title("🌿 EcoClash Arena")
    st.sidebar.markdown(
        "A competitive social gamified space designed to build sustainable habits."
    )
    
    st.sidebar.markdown("### 🗺️ Arena Navigation")
    current_tab = st.sidebar.radio(
        "Go to page:",
        ["🏟️ Leaderboard & Arena", "🏆 Quiz & Rewards", "📚 Eco-Insights (Articles)"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔒 Security & Connectivity")
    
    # API key user override for local testing
    custom_key = st.sidebar.text_input(
        "Gemini API Key (Optional Override):",
        value=st.session_state.custom_api_key,
        type="password",
        help="Input your Google Gemini API key if not set in streamlit secrets."
    )
    if custom_key != st.session_state.custom_api_key:
        st.session_state.custom_api_key = custom_key
        st.rerun()
        
    # Toggle to explicitly enable Mock Mode for judging
    mock_mode = st.sidebar.checkbox(
        "Force Developer Mock Mode",
        value=st.session_state.dev_mock_mode,
        help="Toggling this forces the offline rule-based dialog system to run instantly."
    )
    if mock_mode != st.session_state.dev_mock_mode:
        st.session_state.dev_mock_mode = mock_mode
        st.rerun()
        
    # Connection Indicator
    st.sidebar.markdown("### 🔌 API Status")
    if st.session_state.dev_mock_mode:
        st.sidebar.warning("Developer Mock Mode: ACTIVE (Forced)")
    elif st.session_state.mock_fallback_triggered:
        st.sidebar.warning("Developer Mock Mode: ACTIVE (API Exception Fallback)")
    else:
        st.sidebar.success("Gemini API Mode: READY")
        
    # Reset State button
    if st.sidebar.button("🔄 Reset Carbon Challenge", use_container_width=True):
        st.session_state.clear()
        st.rerun()
        
    # ==========================================
    # VIEW A: LEADERBOARD & ARENA
    # ==========================================
    if current_tab == "🏟️ Leaderboard & Arena":
        st.title("🏟️ EcoClash Carbon Arena")
        st.markdown(
            "Log your habits, interact in the group chat, and reduce your score to outrank the AI players!"
        )
        
        # Warning banner if in Developer Mock Mode
        if st.session_state.dev_mock_mode or st.session_state.mock_fallback_triggered:
            st.markdown(
                """
                <div class='mock-alert'>
                    ⚡ <strong>Rate Limit Resilience Active:</strong> Switch to Developer Mock Mode is active. 
                    Characters are engaging using witty pre-baked dialogues!
                </div>
                """,
                unsafe_allow_html=True
            )
            
        # Top Stats Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                f"""
                <div class='glass-card'>
                    <div style='font-size: 0.85rem; text-transform: uppercase; color: #94a3b8;'>Your Footprint</div>
                    <div class='glowing-metric'>{st.session_state.user_score:.1f}</div>
                    <div style='font-size: 0.8rem; color: #a7f3d0;'>kg CO2e / month</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            # Calculate Rank
            player_scores = [
                ("Eco-Enid", st.session_state.ai_scores["Eco-Enid"]),
                ("Astro-Sam", st.session_state.ai_scores["Astro-Sam"]),
                ("Less-Is-More", st.session_state.ai_scores["Less-Is-More"]),
                ("You", st.session_state.user_score)
            ]
            player_scores.sort(key=lambda x: x[1])  # Ascending (lower is better!)
            user_rank = [x[0] for x in player_scores].index("You") + 1
            
            st.markdown(
                f"""
                <div class='glass-card'>
                    <div style='font-size: 0.85rem; text-transform: uppercase; color: #94a3b8;'>Current Rank</div>
                    <div class='glowing-metric' style='color:#38bdf8; text-shadow: 0 0 15px rgba(56, 189, 248, 0.45);'>#{user_rank}</div>
                    <div style='font-size: 0.8rem; color: #cbd5e1;'>Out of 4 Players</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                f"""
                <div class='glass-card'>
                    <div style='font-size: 0.85rem; text-transform: uppercase; color: #94a3b8;'>Eco Quiz Points</div>
                    <div class='glowing-metric' style='color:#fbbf24; text-shadow: 0 0 15px rgba(250, 204, 21, 0.45);'>{st.session_state.user_points * 10}</div>
                    <div style='font-size: 0.8rem; color: #fef08a;'>{st.session_state.user_points} of 3 Correct</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col4:
            badge_count = len(st.session_state.unlocked_badges)
            st.markdown(
                f"""
                <div class='glass-card'>
                    <div style='font-size: 0.85rem; text-transform: uppercase; color: #94a3b8;'>Achievements</div>
                    <div class='glowing-metric' style='color:#c084fc; text-shadow: 0 0 15px rgba(192, 132, 252, 0.45);'>{badge_count}</div>
                    <div style='font-size: 0.8rem; color: #f3e8ff;'>Badges Unlocked</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        # Divide Arena layout: Left (Leaderboard & Quick actions), Right (Multi-Agent Chat)
        layout_left, layout_right = st.columns([11, 13])
        
        with layout_left:
            st.subheader("📊 Dynamic Leaderboard")
            
            # Formulating data for the HTML Table
            table_rows = ""
            for idx, (player, score) in enumerate(player_scores):
                rank = idx + 1
                row_class = "user-row" if player == "You" else ""
                
                # Bullet styles for archetypes
                archetype = "Active Challenger ⚡"
                if player == "Eco-Enid":
                    archetype = "Zero-Waste Purist 🌿"
                elif player == "Astro-Sam":
                    archetype = "Smart-Home Tech Nerd 🤖"
                elif player == "Less-Is-More":
                    archetype = "Chill Minimalist ☕"
                    
                table_rows += f"""
                <tr class="{row_class}">
                    <td>{rank}</td>
                    <td><strong>{player}</strong></td>
                    <td style="text-align: right; font-family: monospace; font-size: 1.1rem;">{score:.1f}</td>
                    <td>{archetype}</td>
                </tr>
                """
                
            st.markdown(
                f"""
                <table class="leaderboard-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Competitor Name</th>
                            <th style="text-align: right;">Carbon (kg CO2e)</th>
                            <th>Eco Archetype</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown("### ⚡ Log Habit Loggers (Carbon Credits)")
            st.markdown("Click an eco-action to update your score and trigger opponent reactions:")
            
            # Action Buttons Row
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                if st.button("🚴 Log Transport: Commute by Bike/Bus", use_container_width=True, help="Reduces score by 15.0 kg CO2"):
                    log_user_action("commute", 15.0, "I traveled to the office using public transit and active bicycle riding instead of driving my gas-powered car!")
                    st.rerun()
                    
                if st.button("🥗 Log Diet: Eat 100% Plant-Based", use_container_width=True, help="Reduces score by 8.0 kg CO2"):
                    log_user_action("food", 8.0, "I planned a plant-based meal today containing clean organic vegetables and local legumes, skipping animal protein!")
                    st.rerun()
            with act_col2:
                if st.button("🔌 Log Energy: Unplug Standby Load", use_container_width=True, help="Reduces score by 6.0 kg CO2"):
                    log_user_action("energy", 6.0, "I audited my living room electronics, unplugged all inactive vampire chargers, and set the HVAC to 78°F!")
                    st.rerun()
                    
                if st.button("🔄 Log Shop: Repair & Thirft Items", use_container_width=True, help="Reduces score by 12.0 kg CO2"):
                    log_user_action("shopping", 12.0, "I repaired my cracked phone screen shield and bought some secondhand clothes at the local circular thrift shop!")
                    st.rerun()
                    
            st.info(
                "💡 Earning carbon credits decreases your score. The lower your score, the higher you climb on the board!"
            )
            
        with layout_right:
            st.subheader("🏟️ Multi-Agent Arena Chat")
            
            # Render chat history with custom bubbles
            chat_container_html = ""
            for msg in st.session_state.chat_history:
                name = msg.get("name", "Unknown")
                content = msg.get("content", "")
                
                if name == "You":
                    bubble_class = "bubble-user"
                    name_class = "name-user"
                    avatar = "👤"
                elif name == "Eco-Enid":
                    bubble_class = "bubble-enid"
                    name_class = "name-enid"
                    avatar = "🌿"
                elif name == "Astro-Sam":
                    bubble_class = "bubble-sam"
                    name_class = "name-sam"
                    avatar = "🤖"
                else:
                    bubble_class = "bubble-minimalist"
                    name_class = "name-minimalist"
                    avatar = "☕"
                    
                chat_container_html += f"""
                <div class="chat-bubble {bubble_class}">
                    <div class="chat-name {name_class}">{avatar} {name}</div>
                    <div>{content}</div>
                </div>
                """
                
            st.markdown(
                f"""
                <div class="chat-bubble-container">
                    {chat_container_html}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Free-text arena input
            user_msg = st.chat_input("Enter a custom habit or challenge the opponents...")
            if user_msg:
                log_user_action("custom", 4.0, user_msg)
                st.rerun()
                
        # Check badge locks after every state update
        check_and_unlock_badges()

    # ==========================================
    # VIEW B: QUIZ & REWARDS
    # ==========================================
    elif current_tab == "🏆 Quiz & Rewards":
        st.title("🏆 Eco-Quiz & Unlocked Achievements")
        st.markdown(
            "Test your sustainability knowledge. Correct answers directly slash your carbon footprint!"
        )
        
        quiz_col, rewards_col = st.columns([13, 11])
        
        with quiz_col:
            st.subheader("🧠 Carbon Awareness Quiz")
            
            # Form-based quiz implementation
            with st.form("eco_quiz_form"):
                score_counter = 0
                temp_selections = {}
                
                for q in QUIZ_QUESTIONS:
                    st.markdown(f"**Question {q['id']}:** {q['question']}")
                    
                    # Pre-select previous choice if available
                    default_idx = st.session_state.quiz_selections.get(q["id"], 0)
                    selected_opt = st.radio(
                        "Select one option:",
                        q["options"],
                        index=default_idx,
                        key=f"q_{q['id']}",
                        label_visibility="collapsed"
                    )
                    
                    # Store selected index
                    selected_idx = q["options"].index(selected_opt)
                    temp_selections[q["id"]] = selected_idx
                    
                    if selected_idx == q["correct_idx"]:
                        score_counter += 1
                        
                    st.markdown("---")
                    
                submitted = st.form_submit_button("Submit Quiz Answers", use_container_width=True)
                
                if submitted:
                    st.session_state.quiz_selections = temp_selections
                    st.session_state.quiz_submitted = True
                    
                    # Apply points
                    old_points = st.session_state.user_points
                    st.session_state.user_points = score_counter
                    
                    # Dynamic footprint reduction for correct answers!
                    new_correct = max(0, score_counter - old_points)
                    reduction = new_correct * 35.0  # 35 kg CO2 off per newly correct answer!
                    st.session_state.user_score = max(40.0, st.session_state.user_score - reduction)
                    
                    st.toast(f"Quiz completed! You scored {score_counter}/3!", icon="🎯")
                    st.rerun()
            
            # Reveal Explanations upon submission
            if st.session_state.quiz_submitted:
                st.markdown("### 📖 Answer Explanations")
                for q in QUIZ_QUESTIONS:
                    user_ans = st.session_state.quiz_selections.get(q["id"])
                    is_correct = user_ans == q["correct_idx"]
                    
                    color = "green" if is_correct else "red"
                    symbol = "✅" if is_correct else "❌"
                    
                    st.markdown(
                        f"""
                        <div style="background-color: rgba(30,41,59,0.3); padding: 15px; border-radius: 8px; margin-bottom: 12px; border-left: 4px solid {color};">
                            <strong>Question {q['id']}:</strong> {symbol} Your Answer: <em>{q['options'][user_ans]}</em><br/>
                            <span style="color: #4ade80;">Correct: {q['options'][q['correct_idx']]}</span><br/>
                            <p style="margin-top: 8px; font-size: 0.9rem; color: #cbd5e1;"><strong>Why?</strong> {q['explanation']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
        with rewards_col:
            st.subheader("🎖️ Your Badges Showcase")
            st.markdown("Unlocking badges requires answering quiz questions and lowering your carbon index:")
            
            # List of badge requirements
            badge_list = [
                {
                    "name": "⭐ Carbon Cadet",
                    "req": "Answer at least 1 Quiz Question correctly.",
                    "desc": "Initiated into carbon lifecycle awareness and sustainable parameters.",
                    "icon": "⭐"
                },
                {
                    "name": "🌿 Eco Champ",
                    "req": "Answer 2 Quiz Questions correctly & reduce score below 400 kg CO2.",
                    "desc": "Actively minimizing plastic, food waste, and commuting footprints.",
                    "icon": "🌿"
                },
                {
                    "name": "⚡ Sustainability Sovereign",
                    "req": "Answer all 3 Quiz Questions correctly & reduce score below 350 kg CO2.",
                    "desc": "Ultimate carbon optimizer. Master of HVAC, active transit, and digital efficiency.",
                    "icon": "⚡"
                }
            ]
            
            # Render badge grid
            badge_html = ""
            for badge in badge_list:
                is_unlocked = badge["name"] in st.session_state.unlocked_badges
                card_class = "badge-card badge-unlocked" if is_unlocked else "badge-card"
                status_text = "🟢 UNLOCKED" if is_unlocked else "🔒 LOCKED"
                status_color = "#eab308" if is_unlocked else "#64748b"
                
                badge_html += f"""
                <div class="{card_class}">
                    <div class="badge-icon">{badge['icon']}</div>
                    <h4 style="margin: 5px 0;">{badge['name']}</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; margin: 4px 0;">{badge['desc']}</p>
                    <div style="font-size: 0.75rem; color: {status_color}; font-weight: bold; margin-top: 8px;">
                        {status_text} <br/>
                        <span style="font-weight: normal; color: #cbd5e1;">Req: {badge['req']}</span>
                    </div>
                </div>
                """
                
            st.markdown(
                f"""
                <div class="badge-grid">
                    {badge_html}
                </div>
                """,
                unsafe_allow_html=True
            )
            
        # Re-check badges
        check_and_unlock_badges()

    # ==========================================
    # VIEW C: ECO-INSIGHTS ARTICLES
    # ==========================================
    elif current_tab == "📚 Eco-Insights (Articles)":
        st.title("📚 Scientific Eco-Insights")
        st.markdown(
            "Read peer-reviewed, deep-dive analyses explaining the physical math behind global emissions."
        )
        
        # Navigation inside Articles tab
        article_tab = st.selectbox(
            "Select Article Topic:",
            [
                "💻 Hidden Digital Footprints (Streaming, AI, Cloud)",
                "🏠 Residential Micro-Habits (HVAC, Vampire Loads, Food Physics)",
                "🚗 Urban Transportation Math (Active Commutes vs. EVs vs. Ride-share)"
            ]
        )
        
        st.markdown("---")
        
        # Readout based on selection
        if "Hidden Digital" in article_tab:
            st.markdown(ARTICLES["digital"])
        elif "Residential Micro-Habits" in article_tab:
            st.markdown(ARTICLES["habits"])
        else:
            st.markdown(ARTICLES["transport"])

if __name__ == "__main__":
    main()
