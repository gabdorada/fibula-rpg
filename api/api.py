from fastapi import FastAPI, Query
from database import Database
import httpx

app = FastAPI(title="Fibula RPG API")


@app.get("/")
def root():
    return {"status": "ok", "message": "Fibula RPG API is running"}


def map_weather_to_rpg(temperature_c: float | None, weather_code: int | None) -> dict:
    if weather_code in (95, 96, 99):
        return {
            "condition": "storm",
            "label": "Arcane & Lightning Storm",
            "effect": "Electric and storm attacks gain +20% impact; visibility is reduced.",
        }
    if weather_code in (51, 53, 55, 61, 63, 65, 80, 81, 82):
        return {
            "condition": "rain",
            "label": "Steady Rain",
            "effect": "Fire damage loses strength (-15%) and the ground becomes slippery.",
        }
    if weather_code in (45, 48):
        return {
            "condition": "fog",
            "label": "Dense Fog",
            "effect": "Ambushed enemies gain stealth advantage; ranged attacks take a penalty.",
        }
    if temperature_c is not None and temperature_c >= 30:
        return {
            "condition": "heatwave",
            "label": "Scorching Heat",
            "effect": "Fatigue sets in faster; potions and rest carry extra value.",
        }
    if temperature_c is not None and temperature_c <= 8:
        return {
            "condition": "cold",
            "label": "Biting Cold",
            "effect": "Slower movement early in combat; rapid cooling.",
        }
    return {
        "condition": "clear",
        "label": "Clear Skies",
        "effect": "Balanced conditions for exploring and fighting with no negative modifiers.",
    }


@app.get("/world/weather")
def get_weather(lat: float = -25.4284, lon: float = -49.2733):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,weather_code",
    }

    with httpx.Client(timeout=10.0) as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    current = data.get("current", {})
    temperature_c = current.get("temperature_2m")
    weather_code = current.get("weather_code")
    rpg_weather = map_weather_to_rpg(temperature_c, weather_code)

    return {
        "coordinates": {"lat": lat, "lon": lon},
        "temperature_c": temperature_c,
        "weather_code": weather_code,
        "rpg_weather": rpg_weather,
    }


@app.get("/ranking")
def get_ranking(limit: int = Query(default=10, ge=1, le=50)):
    db = Database()
    try:
        ranking = db.get_ranking(limit=limit)
    finally:
        db.close()

    return {
        "count": len(ranking),
        "ranking": ranking,
    }