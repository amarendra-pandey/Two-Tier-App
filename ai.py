from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = genai.Client(api_key=API_KEY)

def suggest_task(goal: str):
    try:
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = (
                f"Give 5 short task for: {goal}"
                "Each task must be one short sentence."
                "No numbering, no explanation, no markdown, no symbols."
            )
        )

        lines = response.text.split("\n")

        return [line.strip() for line in lines if line.strip()]

    except Exception as e:
        print("AI failed:", e)
        return ["Try again later"]