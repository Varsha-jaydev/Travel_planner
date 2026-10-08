"""
Travel Planner Agent using CrewAI.

Multi-agent crew that creates personalized travel itineraries:
- Destination Researcher: gathers destination info
- Activity Planner: creates day-by-day activities
- Budget Analyst: estimates costs

Can be used from:
1. Command line
2. Streamlit frontend
"""

import argparse

from crewai import Agent, Crew, Process, Task, LLM
from dotenv import load_dotenv

load_dotenv()


def build_travel_crew(
    destination: str,
    days: int,
    budget: float,
    interests: str,
) -> str:

    # -------------------------
    # Validate input
    # -------------------------

    if not destination.strip():
        raise ValueError("Destination is required.")

    if days < 1:
        raise ValueError("Days must be at least 1.")

    if budget <= 0:
        raise ValueError("Budget must be greater than 0.")

    if not interests.strip():
        interests = "food, culture, history"

    # -------------------------
    # Local Ollama LLM
    # -------------------------

    llm = LLM(
        model="ollama/qwen3:8b",
        base_url="http://localhost:11434",
        temperature=0.4,
    )

    # -------------------------
    # AGENTS
    # -------------------------

    researcher = Agent(
        role="Destination Researcher",
        goal=(
            f"Research {destination} and provide accurate, "
            "useful travel insights."
        ),
        backstory=(
            "Expert travel journalist who has visited 100+ countries. "
            "Knows the best attractions, hidden gems, local food, "
            "neighborhoods, transportation and practical travel tips."
        ),
        llm=llm,
        verbose=False,
    )

    planner = Agent(
        role="Travel Itinerary Planner",
        goal=(
            f"Create a detailed {days}-day itinerary "
            f"for {destination}."
        ),
        backstory=(
            "Experienced travel consultant who specializes in "
            "creating realistic, enjoyable and personalized itineraries."
        ),
        llm=llm,
        verbose=False,
    )

    budget_analyst = Agent(
        role="Travel Budget Analyst",
        goal=(
            f"Estimate realistic travel costs for {destination} "
            f"while staying within a ${budget:.2f} budget."
        ),
        backstory=(
            "Financial travel advisor who helps travelers "
            "maximize experiences while staying within budget."
        ),
        llm=llm,
        verbose=False,
    )

    # -------------------------
    # RESEARCH TASK
    # -------------------------

    research_task = Task(
        description=f"""
Research {destination} for a {days}-day trip.

Traveler interests:
{interests}

Cover:

1. Best time to visit
2. Best neighborhoods to stay in
3. Must-see attractions
4. Hidden gems
5. Local food and dishes
6. Recommended restaurants or food areas
7. Public transportation
8. Approximate travel times between major areas
9. Cultural customs
10. Practical travel tips

Focus on information that will help another agent
create a realistic itinerary.
""",
        agent=researcher,
        expected_output=(
            "A detailed destination research brief covering "
            "areas, attractions, food, transportation, "
            "customs and practical tips."
        ),
    )

    # -------------------------
    # ITINERARY TASK
    # -------------------------

    planning_task = Task(
        description=f"""
Create a realistic {days}-day itinerary for:

Destination:
{destination}

Total budget:
${budget:.2f}

Traveler interests:
{interests}

Use the destination research provided by the researcher. Keep in mind the travelers interests.

For every day include:

- Morning activity
- Lunch recommendation
- Afternoon activity
- Dinner recommendation
- Evening activity
- Approximate travel time between locations
- Approximate daily cost

Requirements:

- Group nearby attractions together.
- Avoid unrealistic travel schedules.
- Include breaks/free time.
- Prioritize the traveler's interests.
- Include specific restaurant recommendations.
- Keep the itinerary within the overall budget.
- Make the itinerary practical for a real traveler.

Format the response clearly using Markdown.
""",
        agent=planner,
        expected_output=(
            f"A detailed {days}-day Markdown itinerary "
            "with morning, lunch, afternoon, dinner, evening, "
            "travel times and estimated costs."
        ),
        context=[research_task],
    )

    # -------------------------
    # BUDGET TASK
    # -------------------------

    budget_task = Task(
        description=f"""
Create a detailed budget for a {days}-day trip to {destination}.

Total budget:
${budget:.2f}

Traveler interests:
{interests}

Use the destination research and proposed itinerary.

Include estimates for:

1. Flights
2. Accommodation
3. Food
4. Activities
5. Local transportation
6. Miscellaneous expenses

Provide:

- Total estimated cost
- Cost per day
- Cost by category
- Remaining budget
- Whether the budget is realistic
- Money-saving recommendations

If the budget is too low, clearly explain why
and suggest realistic adjustments.

Format the result using Markdown.
""",
        agent=budget_analyst,
        expected_output=(
            "An itemized Markdown budget breakdown with "
            "category totals, daily averages, total cost, "
            "remaining budget and money-saving tips."
        ),
        context=[research_task, planning_task],
    )

    # -------------------------
    # CREW
    # -------------------------

    crew = Crew(
        agents=[
            researcher,
            planner,
            budget_analyst,
        ],
        tasks=[
            research_task,
            planning_task,
            budget_task,
        ],
        process=Process.sequential,
        verbose=False,
    )

    # -------------------------
    # RUN CREW
    # -------------------------

    result = crew.kickoff()

    return str(result)


# ============================================================
# COMMAND LINE VERSION
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="AI Travel Planner"
    )

    parser.add_argument(
        "--destination",
        default="Tokyo, Japan",
        help="Travel destination",
    )

    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days",
    )

    parser.add_argument(
        "--budget",
        type=float,
        default=3000,
        help="Total budget in USD",
    )

    parser.add_argument(
        "--interests",
        default="food, culture, history",
        help="Traveler interests",
    )

    args = parser.parse_args()

    print(
        f"\n✈️ Planning {args.days}-day trip "
        f"to {args.destination} "
        f"(Budget: ${args.budget:,.2f})\n"
    )

    itinerary = build_travel_crew(
        destination=args.destination,
        days=args.days,
        budget=args.budget,
        interests=args.interests,
    )

    print("=" * 60)
    print("🗺️ TRAVEL ITINERARY")
    print("=" * 60)
    print(itinerary)


if __name__ == "__main__":
    main()