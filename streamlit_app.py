import streamlit as st
import os
from dotenv import load_dotenv
import datetime
from src.trip_planner.crew import TripPlannerCrew

# Load environment variables
load_dotenv()

# Streamlit page configuration
st.set_page_config(layout="centered", page_title="AI Trip Planner", page_icon="✈️")

# Title and subtitle
st.title("✈️ AI Trip Planner")
st.markdown("Plan your dream trip with the help of AI!")

# Input fields
origin = st.text_input("What is your origin city?", placeholder="e.g., New York")

cities = st.text_input("What are the cities you are interested in? (comma-separated)", placeholder="e.g., Paris, Rome, London")

today = datetime.date.today()
next_month = today + datetime.timedelta(days=30)
dates = st.date_input(
    "What is the date range you are interested in?",
    value=(today, next_month),
    min_value=today,
    format="YYYY-MM-DD"
)

# Convert date objects to string
if isinstance(dates, tuple) and len(dates) == 2:
    start_date = dates[0].strftime("%Y-%m-%d")
    end_date = dates[1].strftime("%Y-%m-%d")
    date_range = f"{start_date} to {end_date}"
elif isinstance(dates, datetime.date):
    date_range = dates.strftime("%Y-%m-%d")
else:
    date_range = ""

interests = st.text_area("What are your interests?", placeholder="e.g., museums, parks, historical sites")

# Plan button
if st.button("Plan My Trip!"):
    if not all([origin, cities, date_range, interests]):
        st.error("Please fill in all the fields to plan your trip.")
    else:
        st.info("Planning your trip... This might take a few moments.")

        inputs = {
            "origin": origin,
            "cities": cities,
            "range": date_range,
            "interests": interests,
        }

        try:
            TripPlannerCrew().crew().kickoff(inputs=inputs)

            report_path = "output/report.md"
            if os.path.exists(report_path):
                with open(report_path, "r", encoding="utf-8") as f:
                    report_content = f.read()
                st.subheader("Your Trip Plan:")
                st.markdown(report_content)

                st.download_button(
                    label="Download Trip Plan",
                    data=report_content,
                    file_name="trip_plan_report.md",
                    mime="text/markdown"
                )
            else:
                st.warning("Trip plan report not found. Something might have gone wrong.")
        except Exception as e:
            st.error(f"An error occurred during trip planning: {e}")

# Footer
st.markdown("---")
st.caption("Powered by CrewAI and Streamlit")
