from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from src.trip_planner.tools.custom_tool import SearchTools,BrowserTools,CalculatorTools


@CrewBase
class TripPlannerCrew():
    """Research crew for comprehensive topic analysis and reporting"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def city_selection_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['city_selection_agent'], 
            verbose=True,
            tools = [SearchTools(), BrowserTools()]
        )

    @agent
    def local_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['local_expert'], 
            verbose=True,
            tools = [SearchTools(), BrowserTools()]
        )
    
    @agent
    def travel_concierge(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_concierge'],
            verbose=True
        )

    @task
    def identify_task(self) -> Task:
        return Task(
            config=self.tasks_config['identify_task'],
            tools = [SearchTools(), BrowserTools(),CalculatorTools()]
        )

    @task
    def gather_task(self) -> Task:
        return Task(
            config=self.tasks_config['gather_task'], 
            output_file='output/report.md'
        )
    @task
    def plan_task(self) -> Task:
        return Task(
            config=self.tasks_config['plan_task'],
            output_file='output/report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the trip plan crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )