import asyncio
import datetime
import random

from src.mcp_weather_server.a2a_agents.location_agent import LocationAgent
from src.mcp_weather_server.a2a_agents.crop_agent import CropAgent
from src.mcp_weather_server.a2a_agents.weather_agent import WeatherAgent
from src.mcp_weather_server.a2a_agents.alert_agent import AlertAgent


class DailyAlertWorkflow:
    def __init__(self, state, district):
        self.state = state
        self.district = district
        self.location_agent = LocationAgent()
        self.crop_agent = CropAgent()
        self.weather_agent = WeatherAgent()
        self.alert_agent = AlertAgent()
        self.semaphore = asyncio.Semaphore(5)  # limit concurrent weather requests

    async def run(self):
        print(f"--- Starting Daily Alert Workflow for {self.district}, {self.state} ---")
        locations = await self.location_agent.get_locations(self.state, self.district)
        if not locations:
            print("Workflow failed: Could not retrieve locations.")
            return

        # Process each location concurrently with control
        tasks = [self.process_location(location) for location in locations]
        await asyncio.gather(*tasks)
        print("\n--- Daily Alert Workflow Completed ---")

    async def process_location(self, location):
        village = location["village"]
        lat = location["latitude"]
        lon = location["longitude"]
        print(f"\n--- Processing {village} ---")

        # Crop season & dates
        season = self.crop_agent.get_current_season()
        plant_date = "2024-11-01"
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        crop_info_list = await self.crop_agent.get_crop_info(self.state, season, plant_date, current_date)
        if not crop_info_list:
            print(f"Could not get crop info for {village}. Skipping.")
            return

        for crop_info in crop_info_list:
            crop = crop_info["crop"]
            growth_stage = crop_info["growth_stage"]
            print(f"Processing crop: {crop} at stage: {growth_stage}")

            weather_forecast = await self.safe_weather_forecast(lat, lon)
            if not weather_forecast:
                print(f"Could not get weather forecast for {village}. Skipping.")
                continue

            alert = await self.alert_agent.generate_alert(
                crop=crop,
                weather_data=weather_forecast,
                growth_stage=growth_stage,
                latitude=lat,
                longitude=lon
            )

            if alert and "error" not in alert:
                print("\n--- Generated Weather Alert ---")
                print(f"Village: {village}")
                print(f"Crop: {crop}")
                print(f"Alert: {alert['alert']}")
                print(f"Impact: {alert['impact']}")
                print(f"Recommendations: {alert['recommendations']}")
                print("-----------------------------")
            elif alert and "error" in alert:
                print(f"Error generating alert: {alert['error']}")

    async def safe_weather_forecast(self, lat, lon, retries=3):
        for attempt in range(retries):
            try:
                async with self.semaphore:
                    await asyncio.sleep(random.uniform(0.1, 0.4))  # jitter
                    return await self.weather_agent.get_weather_forecast(lat, lon)
            except Exception as e:
                print(f"Error fetching weather for ({lat}, {lon}) [attempt {attempt + 1}/{retries}]: {e}")
                await asyncio.sleep(1.5)
        return None


# Entrypoint
async def main():
    workflow = DailyAlertWorkflow(state="bihar", district="patna")
    await workflow.run()

if __name__ == "__main__":
    asyncio.run(main())
