import os
from fastapi import HTTPException
from openai import OpenAI
from . import open_meteo

async def predict_weather_alert(latitude: float, longitude: float, crops: list[str]):
    """
    Predicts weather alerts for a given location and crops using an OpenAI LLM.

    Args:
        latitude: The latitude of the location.
        longitude: The longitude of the location.
        crops: A list of crops to consider for the prediction.

    Returns:
        A dictionary containing the predicted weather alert.
    """
    try:
        weather_data = await open_meteo.get_weather_forecast(latitude, longitude)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"Error getting weather data: {e.detail}")

    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        crop_list = ", ".join(crops)
        prompt = f"""
        Given the following weather data for a location:
        {weather_data}

        And the following crops being grown in the area:
        {crop_list}

        Please predict any potential weather alerts for these crops in the next 7 days.
        Provide a summary of the potential impact on the crops and any recommended actions.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that predicts weather alerts for farmers."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"alert": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting prediction from OpenAI: {str(e)}")
