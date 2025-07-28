import pytest
from src.mcp_weather_server.a2a_agents import sms_agent, whatsapp_agent, ussd_agent, ivr_agent, telegram_agent

sample_alert = {
  "alert_id": "BH_PAT_001_20250723",
  "timestamp": "2025-07-23T06:00:00Z",
  "location": {
    "village": "Kumhrar",
    "district": "Patna",
    "state": "Bihar",
    "coordinates": [25.5941, 85.1376]
  },
  "crop": {
    "name": "rice",
    "stage": "flowering"
  },
  "alert": {
    "type": "weather_warning",
    "urgency": "high",
    "message": "Heavy rainfall expected in next 2 days. Delay fertilizer application. Ensure proper drainage."
  },
  "alert": {
    "type": "weather_warning",
    "urgency": "high",
    "message": "Heavy rainfall (40-60mm) expected in next 2 days. Delay fertilizer application. Ensure proper drainage.",
    "action_items": ["delay_fertilizer", "check_drainage"],
    "valid_until": "2025-07-25T18:00:00Z"
  },
  "weather": {
    "forecast_days": 3,
    "rain_probability": 85,
    "expected_rainfall": "45mm"
  }
}

def test_sms_agent():
    sms = sms_agent.create_sms_message(sample_alert)
    assert len(sms) <= 160
    assert "भारी वर्षा" in sms

def test_whatsapp_agent():
    whatsapp_message = whatsapp_agent.create_whatsapp_message(sample_alert)
    assert "text" in whatsapp_message
    assert "buttons" in whatsapp_message
    assert "Acknowledge" in whatsapp_message["buttons"][0]["title"]

def test_ussd_agent():
    main_menu = ussd_agent.create_ussd_menu(sample_alert)
    assert "Mausam ki jankari" in main_menu
    submenu = ussd_agent.get_ussd_submenu(sample_alert, 1)
    assert "Chetavani" in submenu

def test_ivr_agent():
    main_script = ivr_agent.create_ivr_script(sample_alert)
    assert len(main_script) > 0
    assert "Namaste" in main_script[0]["text"]
    submenu_script = ivr_agent.get_ivr_submenu_script(sample_alert)
    assert len(submenu_script) > 0
    assert "Salah" in submenu_script[0]["text"]

def test_telegram_agent():
    telegram_message = telegram_agent.create_telegram_message(sample_alert)
    assert "text" in telegram_message
    assert "reply_markup" in telegram_message
    assert "inline_keyboard" in telegram_message["reply_markup"]
    assert "Acknowledge" in telegram_message["reply_markup"]["inline_keyboard"][0][0]["text"]
