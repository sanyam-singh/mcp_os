# MCP Weather Server

The MCP Weather Server is a comprehensive Model Context Protocol (MCP) compliant server designed to provide AI agents with access to real-time and historical weather data. Built using Python and FastAPI, it integrates with multiple weather APIs to deliver accurate, up-to-date meteorological information.

## Key Features

-   **Model Context Protocol (MCP) compliance** for seamless AI agent integration
-   **Dual API integration:** OpenMeteo (free) and Tomorrow.io (premium)
-   **Comprehensive weather data:** current conditions, forecasts, historical data, and alerts
-   **Robust error handling** and data validation
-   **Configurable through environment variables**
-   **Extensive logging and monitoring** capabilities
-   **RESTful API design** with JSON responses
-   **Built-in testing and validation tools**

## Installation & Setup

### Prerequisites

-   Python 3.8 or higher
-   pip package manager
-   Internet connection for API access
-   Optional: Tomorrow.io API key for premium features

### Installation Steps

1.  Clone or download the project files
2.  Install dependencies: `pip install -r requirements.txt`
3.  Copy `.env.example` to `.env`
4.  Configure environment variables (optional Tomorrow.io API key)
5.  Run the server: `python -m mcp_weather_server.server`

## Project Structure

```
mcp-weather-server/
├── src/mcp_weather_server/
│   ├── __init__.py
│   ├── server.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── open_meteo.py
│   │   └── tomorrow_io.py
│   └── utils/
│       ├── __init__.py
│       └── weather_utils.py
├── requirements.txt
├── pyproject.toml
├── .env.example
├── README.md
├── test_server.py
└── examples.py
```
