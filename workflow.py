import asyncio
import datetime
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

    async def run(self):
        print(f"--- Starting Daily Alert Workflow for {self.district}, {self.state} ---")

        # 1. Location Processing
        locations = await self.location_agent.get_locations(self.state, self.district)
        if not locations:
            print("Workflow failed: Could not retrieve locations.")
            return

        for location in locations:
            village = location["village"]
            lat = location["latitude"]
            lon = location["longitude"]
            print(f"\n--- Processing {village} ---")

            # 2. Crop Assessment
            season = self.crop_agent.get_current_season()
            # These dates are for demonstration. In a real scenario, you'd have a way
            # to determine the actual planting dates for each location.
            plant_date = "2024-11-01"
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")

            crop_info_list = await self.crop_agent.get_crop_info(self.state, season, plant_date, current_date)
            if not crop_info_list:
                print(f"Could not get crop info for {village}. Skipping.")
                continue

            for crop_info in crop_info_list:
                crop = crop_info["crop"]
                growth_stage = crop_info["growth_stage"]
                print(f"Processing crop: {crop} at stage: {growth_stage}")

                # 3. Weather Analysis
                weather_forecast = await self.weather_agent.get_weather_forecast(lat, lon)
                if not weather_forecast:
                    print(f"Could not get weather forecast for {village}. Skipping.")
                    continue

                # 4. Alert Generation
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

        print("\n--- Daily Alert Workflow Completed ---")


async def main():
    # Example for Patna, Bihar
    workflow = DailyAlertWorkflow(state="bihar", district="patna")
    await workflow.run()

if __name__ == "__main__":
    asyncio.run(main())
