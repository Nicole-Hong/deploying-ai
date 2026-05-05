
import requests
from openai import OpenAI

client = OpenAI()


def get_weather(city: str) -> str:
    """
    Service 1: API call service.
    Uses Open-Meteo geocoding + weather API.
    """

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    geo_response = requests.get(geo_url, params=geo_params, timeout=10)
    geo_response.raise_for_status()
    geo_data = geo_response.json()

    if "results" not in geo_data or not geo_data["results"]:
        return f"I could not find weather information for {city}."

    location = geo_data["results"][0]
    latitude = location["latitude"]
    longitude = location["longitude"]
    resolved_name = location["name"]
    country = location.get("country", "")

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }

    weather_response = requests.get(weather_url, params=weather_params, timeout=10)
    weather_response.raise_for_status()
    weather_data = weather_response.json()

    current = weather_data.get("current_weather", {})

    temperature = current.get("temperature")
    windspeed = current.get("windspeed")
    winddirection = current.get("winddirection")

    return (
        f"The current weather in {resolved_name}, {country} is about "
        f"{temperature}°C with wind speed around {windspeed} km/h. "
        f"The wind direction is approximately {winddirection} degrees."
    )


def create_project_checklist(project_goal: str) -> str:
    """
    Service 3: Function-calling service.
    The model calls this function when the user asks for a project plan/checklist.
    """

    return f"""
Here is a practical checklist for: {project_goal}

1. Define the user problem clearly.
2. Identify the required data sources.
3. Decide which service should handle the request.
4. Build a simple working prototype first.
5. Add guardrails for restricted topics and prompt attacks.
6. Test the chatbot with realistic user questions.
7. Document the design decisions in the README.
8. Confirm that the app runs from the assignment folder.
9. Push the final files to the assignment-2 branch.
10. Submit the pull request link.
"""


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_project_checklist",
            "description": "Create a structured project checklist for an AI chatbot or software assignment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_goal": {
                        "type": "string",
                        "description": "The project or task the user wants a checklist for."
                    }
                },
                "required": ["project_goal"]
            }
        }
    }
]


def run_function_calling_service(user_message: str) -> str:
    """
    Uses OpenAI function calling.
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are a practical project planning assistant. "
                "Use the available function when the user asks for a checklist, plan, or implementation steps."
            )
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if not message.tool_calls:
        return message.content

    tool_call = message.tool_calls[0]
    args = tool_call.function.arguments

    import json
    parsed_args = json.loads(args)

    if tool_call.function.name == "create_project_checklist":
        return create_project_checklist(parsed_args["project_goal"])

    return "I could not complete the function call."