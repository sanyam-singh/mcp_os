# Bihar AgMCP - Agricultural Weather Alert System Documentation

## Table of Contents
- [System Overview](#system-overview)
- [Architecture](#architecture)
- [Installation & Setup](#installation--setup)
- [Core Components](#core-components)
  - [Server-side](#server-side)
  - [Client-side](#client-side)
- [API Reference](#api-reference)
- [Data Models](#data-models)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## System Overview

### Purpose
The **Bihar AgMCP** (Agricultural Model Control Protocol) is an AI-powered weather alert system designed to provide personalized agricultural advisories to farmers in Bihar, India. The system generates location-specific weather alerts with crop-specific recommendations.

### Key Features
- **AI-Enhanced Weather Alerts:** OpenAI-powered intelligent alert generation  
- **Multi-Channel Communication:** SMS, WhatsApp, USSD, IVR, and Telegram support  
- **Regional Crop Intelligence:** District-specific crop recommendations based on seasons  
- **Real-time Weather Data:** Integration with multiple weather APIs  
- **Geographic Intelligence:** Village-level weather data and coordinates  
- **Web Interface:** User-friendly Gradio interface for easy access  
- **CSV Export:** Data export functionality for analysis  

### Target Users
- Agricultural extension workers
- Farmers and farmer organizations
- Government agricultural departments
- Research institutions
- NGOs working in agriculture

---

## Architecture

### System Architecture Diagram
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Weather APIs │ │ OpenAI API │ │ Geographic APIs │
│ │ │ │ │ │
│ • Open-Meteo │ │ • GPT Models │ │ • Geocoding │
│ • Tomorrow.io │ │ • Alert Gen │ │ • Village Data │
│ • OpenWeather │ │ │ │ │
└─────────────────┘ └─────────────────┘ └─────────────────┘
│ │ │
└───────────────────────┼───────────────────────┘
│
┌─────────────────┐
│ FastAPI Core │
│ │
│ • Alert Engine │
│ • Crop Calendar │
│ • Workflow Mgmt │
└─────────────────┘
│
┌───────────────────────┼───────────────────────┐
│ │ │
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ A2A Agents │ │ Web Interface │ │ API Clients │
│ │ │ │ │ │
│ • SMS Agent │ │ • Gradio UI │ │ • MCP Protocol │
│ • WhatsApp │ │ • CSV Export │ │ • REST API │
│ • USSD/IVR │ │ • District Sel │ │ • JSON-RPC │
│ • Telegram │ │ │ │ │
└─────────────────┘ └─────────────────┘ └─────────────────┘

markdown
Copy
Edit

### Technology Stack
- **Backend:** FastAPI (Python 3.8+)
- **AI:** OpenAI GPT
- **Weather Data:** Open-Meteo, Tomorrow.io, OpenWeatherMap
- **Frontend:** Gradio
- **Data Processing:** Pandas, CSV
- **Async Operations:** asyncio
- **Configuration:** dotenv
- **Logging:** Python logging

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- `pip` package manager
- Internet connection for API access

### Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd bihar-agmcp

# Install dependencies
pip install fastapi uvicorn gradio pandas python-dotenv pydantic
Create environment file
.env file:

env
Copy
Edit
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional Weather APIs
TOMORROW_IO_API_KEY=your_tomorrow_io_key
GOOGLE_WEATHER_API_KEY=your_google_weather_key
OPENWEATHERMAP_API_KEY=your_openweathermap_key
ACCUWEATHER_API_KEY=your_accuweather_key

# Logging
LOG_LEVEL=INFO
Tool dependencies
Ensure the following directories exist:

Copy
Edit
tools/
a2a_agents/
utils/
Quick Start
bash
Copy
Edit
python main.py
Core Components
1. Server-side
a. Alert Generation Engine
Primary Function:
generate_dynamic_alert(district, state) — Generates comprehensive weather alerts for specific districts.

Process Flow:

Village Selection: Randomly selects a village from the district

Coordinate Resolution: Gets GPS coordinates for location

Crop Intelligence: Selects appropriate crop based on:

Current season (Kharif/Rabi/Zaid)

District crop preferences

Regional agricultural patterns

Weather Data Collection: Fetches weather data from APIs

Alert Generation: Creates weather-based alerts

AI Enhancement: Applies OpenAI analysis (if available)

Example:

python
Copy
Edit
alert_data = await generate_dynamic_alert("Patna", "Bihar")
b. Crop Calendar System
Rice (Kharif): June–July planting, October–November harvest

Wheat (Rabi): November–December planting, March–April harvest

Maize (Kharif/Zaid): Dual season crop

Sugarcane (Annual): February–March planting

Mustard (Rabi): October–November planting

District Crop Mapping:

python
Copy
Edit
DISTRICT_CROPS = {
    'patna': {
        'primary': ['rice', 'wheat', 'potato'], 
        'secondary': ['mustard', 'gram'], 
        'specialty': ['sugarcane']
    },
    # ... other districts
}
c. Weather Integration
Supported Weather APIs:

Open-Meteo (Primary)

Tomorrow.io

OpenWeatherMap

AccuWeather

Google Weather

Weather Alert Types:

Heavy Rain Warning (>25mm rainfall)

Moderate Rain Warning (10–25mm rainfall)

Heat/Drought Warning (High temp + low rainfall)

Cold Warning (<10°C)

High Wind Warning (>30 km/h)

Weather Update (Normal conditions)

2. Client-side — A2A Communication Agents
SMS Agent:

python
Copy
Edit
def create_sms_message(alert_data):
    return f"BIHAR ALERT: {crop} in {location} - {weather_summary}"
WhatsApp Agent:

python
Copy
Edit
def create_whatsapp_message(alert_data):
    return {
        "text": formatted_message,
        "buttons": action_buttons
    }
USSD Agent:

python
Copy
Edit
def create_ussd_menu(alert_data):
    return {
        "menu": "CON Weather Alert...\n1. Details\n2. Actions"
    }
IVR Agent:

python
Copy
Edit
def create_ivr_script(alert_data):
    return {
        "script": "Welcome to Bihar weather alert...",
        "menu_options": [...]
    }
Telegram Agent:

python
Copy
Edit
def create_telegram_message(alert_data):
    return {
        "text": message,
        "reply_markup": inline_keyboard
    }
API Reference
Core Endpoints
1. Workflow Execution

http
Copy
Edit
POST /api/run-workflow
Request:

json
Copy
Edit
{
    "state": "bihar",
    "district": "patna"
}
Response:

json
Copy
Edit
{
    "message": "workflow_results",
    "status": "success",
    "csv": "csv_data",
    "raw_data": {
        "alert_data": {...},
        "agent_responses": {...}
    }
}
2. Health Check

http
Copy
Edit
GET /api/health
Response:

json
Copy
Edit
{
    "status": "healthy",
    "openai_available": true,
    "timestamp": "2025-08-13T10:30:00"
}
3. MCP Tool Execution

http
Copy
Edit
POST /mcp
Request:

json
Copy
Edit
{
    "tool": "get_current_weather",
    "parameters": {
        "latitude": 25.5941,
        "longitude": 85.1376
    }
}
4. Geographic Data

swift
Copy
Edit
GET /api/districts/{state}
GET /api/villages/{state}/{district}
5. Weather Data

swift
Copy
Edit
GET /api/weather/{latitude}/{longitude}
Data Models
AlertRequest

python
Copy
Edit
class AlertRequest(BaseModel):
    alert_json: dict
WorkflowRequest

python
Copy
Edit
class WorkflowRequest(BaseModel):
    state: str
    district: str
MCPRequest

python
Copy
Edit
class MCPRequest(BaseModel):
    tool: str
    parameters: dict
Alert Data Structure

json
Copy
Edit
{
    "alert_id": "BH_PAT_VIL_20250813_103000",
    "timestamp": "2025-08-13T10:30:00Z",
    "location": {
        "village": "Danapur",
        "district": "Patna",
        "state": "Bihar",
        "coordinates": [25.5941, 85.1376],
        "coordinates_source": "village_danapur"
    },
    "crop": {
        "name": "rice",
        "stage": "Tillering",
        "season": "kharif",
        "planted_estimate": "2025-06-15"
    },
    "alert": {
        "type": "heavy_rain_warning",
        "urgency": "high",
        "message": "Heavy rainfall expected...",
        "action_items": ["delay_fertilizer", "check_drainage"],
        "ai_generated": true
    },
    "weather": {
        "temperature": "28.5°C",
        "expected_rainfall": "35.2mm",
        "wind_speed": "15.3 km/h",
        "rain_probability": "85%"
    }
}
Configuration
Environment Variables

Required:
OPENAI_API_KEY

Optional:
TOMORROW_IO_API_KEY, GOOGLE_WEATHER_API_KEY, OPENWEATHERMAP_API_KEY, ACCUWEATHER_API_KEY
LOG_LEVEL

CORS Configuration:

python
Copy
Edit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mcp-ui.vercel.app", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"]
)
Bihar Districts Supported:
Patna, Gaya, Bhagalpur, Muzaffarpur, Darbhanga, Siwan, Begusarai, Katihar, Nalanda, Rohtas, … (39 total)

Deployment
Local Development
bash
Copy
Edit
python main.py
# FastAPI server: http://localhost:8000
# Gradio interface: http://localhost:7860
Docker Deployment
dockerfile
Copy
Edit
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000 7860

CMD ["python", "main.py"]
HuggingFace Spaces
python
Copy
Edit
if os.getenv("SPACE_ID") or os.getenv("GRADIO_SERVER_NAME"):
    # HuggingFace Spaces mode
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    demo.launch(server_name="0.0.0.0", server_port=7860)
Troubleshooting
Common Issues

OpenAI API Key Missing
Solution: Add OPENAI_API_KEY to .env

Weather API Failures

Check internet connectivity

Verify API keys

Check API quotas

Geographic Data Issues

Verify district spelling

Check BIHAR_DISTRICTS list

Import Errors

Ensure required modules exist: tools/, a2a_agents/, utils/

Enable Debug Logging

bash
Copy
Edit
export LOG_LEVEL=DEBUG
python main.py
Performance Optimization

API Response Caching with Redis

Database Integration with PostgreSQL/MongoDB

Contributing
Development Guidelines

Follow PEP 8

Use type hints

Add docstrings

Max line length: 100 chars

Testing Example:

python
Copy
Edit
def test_crop_selection():
    crop = select_regional_crop("patna", "bihar")
    assert crop in ["rice", "wheat", "potato"]
Adding New Features

New Weather Provider → tools/new_weather_api.py

New Communication Channel → a2a_agents/slack_agent.py

New Crop Types → Update CROP_CALENDAR

Last Updated: August 13, 2025