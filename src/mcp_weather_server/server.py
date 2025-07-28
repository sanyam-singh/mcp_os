import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import dotenv_values

from .tools import open_meteo, tomorrow_io, google_weather, openweathermap, accuweather, openai_llm, geographic_tools, crop_calendar_tools, alert_generation_tools
from .a2a_agents import sms_agent, whatsapp_agent, ussd_agent, ivr_agent, telegram_agent
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

class AlertRequest(BaseModel):
    alert_json: dict

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
            api_key = config.get("GOOGLE_WEATHER_API_KEY")
            result = await getattr(google_weather, request.tool)(**request.parameters, api_key=api_key)
        elif tool_config["module"] == "openweathermap":
            api_key = config.get("OPENWEATHERMAP_API_KEY")
            result = await getattr(openweathermap, request.tool)(**request.parameters, api_key=api_key)
        elif tool_config["module"] == "accuweather":
            api_key = config.get("ACCUWEATHER_API_KEY")
            result = await getattr(accuweather, request.tool)(**request.parameters, api_key=api_key)
        elif tool_config["module"] == "openai_llm":
            api_key = config.get("OPENAI_API_KEY")
            result = await getattr(openai_llm, request.tool)(**request.parameters, api_key=api_key)
        elif tool_config["module"] == "geographic_tools":
            result = await getattr(geographic_tools, request.tool)(**request.parameters)
        elif tool_config["module"] == "crop_calendar_tools":
            result = await getattr(crop_calendar_tools, request.tool)(**request.parameters)
        elif tool_config["module"] == "alert_generation_tools":
            api_key = config.get("OPENAI_API_KEY")
            result = await getattr(alert_generation_tools, request.tool)(**request.parameters, api_key=api_key)
        else:
            raise HTTPException(status_code=500, detail="Invalid tool module")

        logger.info(f"Successfully executed tool: {request.tool}")
        return result
    except Exception as e:
        logger.exception(f"Error executing tool: {request.tool}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/a2a/sms")
async def a2a_sms_endpoint(request: AlertRequest):
    return {"message": sms_agent.create_sms_message(request.alert_json)}

@app.post("/a2a/whatsapp")
async def a2a_whatsapp_endpoint(request: AlertRequest):
    return whatsapp_agent.create_whatsapp_message(request.alert_json)

@app.post("/a2a/ussd")
async def a2a_ussd_endpoint(request: AlertRequest):
    return {"menu": ussd_agent.create_ussd_menu(request.alert_json)}

@app.post("/a2a/ivr")
async def a2a_ivr_endpoint(request: AlertRequest):
    return {"script": ivr_agent.create_ivr_script(request.alert_json)}

@app.post("/a2a/telegram")
async def a2a_telegram_endpoint(request: AlertRequest):
    return telegram_agent.create_telegram_message(request.alert_json)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
