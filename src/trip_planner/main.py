#!/usr/bin/env python
import sys
import warnings
from trip_planner.crew import TripPlannerCrew
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    origin = input("What is your origin city?\n")
    cities = input("What are the cities you are interested in?\n")
    date_range = input("What is the date range you are interested in?\n")
    interests = input("What are your interests? (e.g., museums, parks, historical sites)\n")

    inputs = {
        "origin": origin,
        "cities": cities,
        "range": date_range,      
        "interests": interests
        }
    
    try:
        TripPlannerCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    origin = input("What is your origin city?\n")
    cities = input("What are the cities you are interested in?\n")
    date_range = input("What is the date range you are interested in?\n")
    interests = input("What are your interests? (e.g., museums, parks, historical sites)\n")

    inputs = {
        "origin": origin,
        "cities": cities,
        "range": date_range,      
        "interests": interests
        }
    try:
        TripPlannerCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TripPlannerCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    origin = input("What is your origin city?\n")
    cities = input("What are the cities you are interested in?\n")
    date_range = input("What is the date range you are interested in?\n")
    interests = input("What are your interests? (e.g., museums, parks, historical sites)\n")

    inputs = {
        "origin": origin,
        "cities": cities,
        "range": date_range,      
        "interests": interests
        }
    
    try:
        TripPlannerCrew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

