import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import dotenv_values

from .tools import open_meteo, tomorrow_io, google_weather, openweathermap, accuweather
from .utils.weather_utils import get_tool_config

config = dotenv_values(".env")

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI()

class MCPRequest(BaseModel):
    tool: str
    parameters: dict

@app.post("/mcp")
async def mcp_endpoint(request: MCPRequest):
    logger.info(f"Received request for tool: {request.tool}")
    tool_config = get_tool_config(request.tool)

    if not tool_config:
        logger.error(f"Tool not found: {request.tool}")
        raise HTTPException(status_code=404, detail="Tool not found")

    try:
        if tool_config["module"] == "open_meteo":
            result = await getattr(open_meteo, request.tool)(**request.parameters)
        elif tool_config["module"] == "tomorrow_io":
            api_key = config.get("TOMORROW_IO_API_KEY")
            result = await getattr(tomorrow_io, request.tool)(**request.parameters, api_key=api_key)
        elif tool_config["module"] == "google_weather":
            api_key = config.get("SERPAPI_API_KEY")
            result = await getattr(google_weather, request.tool)(**request.parameters, api_key=api_key)
        elif tool_config["module"] == "openweathermap":
            api_key = config.get("OPENWEATHERMAP_API_KEY")
            result = await getattr(openweathermap, request.tool)(**request.parameters, api_key=api_key)
        elif tool_config["module"] == "accuweather":
            api_key = config.get("ACCUWEATHER_API_KEY")
            result = await getattr(accuweather, request.tool)(**request.parameters, api_key=api_key)
        else:
            raise HTTPException(status_code=500, detail="Invalid tool module")

        logger.info(f"Successfully executed tool: {request.tool}")
        return result
    except Exception as e:
        logger.exception(f"Error executing tool: {request.tool}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
