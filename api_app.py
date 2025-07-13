from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.trip_planner.crew import TripPlannerCrew

app = FastAPI(
    title="AI Trip Planner API",
    description="API for generating trip plans using CrewAI.",
    version="1.0.0",
)

class TripRequest(BaseModel):
    origin: str
    cities: str
    date_range: str
    interests: str

@app.post("/plan_trip")
async def plan_trip(request: TripRequest):
    """Generate a trip plan based on user inputs."""
    inputs = {
        "origin": request.origin,
        "cities": request.cities,
        "range": request.date_range,
        "interests": request.interests,
    }

    try:
        # Ensure the output directory exists
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        report_path = os.path.join(output_dir, "report.md")

        # Run the CrewAI process
        # Note: CrewAI's kickoff method might write directly to a file
        # or return content. Assuming it writes to output/report.md as per your setup.
        TripPlannerCrew().crew().kickoff(inputs=inputs)

        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                report_content = f.read()
            return {"status": "success", "trip_plan": report_content}
        else:
            raise HTTPException(status_code=500, detail="Trip plan report not found after generation.")

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error during trip planning: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during trip planning: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "AI Trip Planner API is running."}
